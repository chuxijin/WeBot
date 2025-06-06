#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import logging
import os
import re
import time
from collections import defaultdict
from datetime import datetime
from pathlib import PurePosixPath
from typing import Any, Dict, List, Optional, Pattern, Set, Tuple, Union

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.coulddrive.model.filesync import SyncConfig, SyncTask, SyncTaskItem
from backend.app.coulddrive.schema.enum import DriveType, ItemType, MatchMode, MatchTarget, RecursionSpeed, SyncMethod
from backend.app.coulddrive.schema.file import (
    BaseFileInfo,
    DiskTargetDefinition,
    ExclusionRuleDefinition,
    GetCompareDetail,
    RenameRuleDefinition,
    ShareSourceDefinition,
    ListFilesParam,
    ListShareFilesParam,
    TransferParam,
    RemoveParam,
    MkdirParam,
)
from backend.app.coulddrive.schema.filesync import GetSyncConfigDetail
from backend.app.coulddrive.schema.user import GetDriveAccountDetail
from backend.app.coulddrive.service.yp_service import get_drive_manager

logger = logging.getLogger(__name__)

class FileSyncService:
    """文件同步服务"""
    
    def __init__(self):
        """初始化文件同步服务"""
        # 移除重复的客户端缓存，直接使用全局管理器
        pass
    
    def _parse_sync_method(self, method_str: str) -> str:
        """解析同步方式
        
        Args:
            method_str: 同步方式字符串
            
        Returns:
            str: 标准化的同步方式
        """
        # 尝试匹配枚举值
        method_lower = method_str.lower() if method_str else ""
        
        if method_lower == "incremental":
            return SyncMethod.INCREMENTAL.value
        elif method_lower == "full":
            return SyncMethod.FULL.value
        elif method_lower == "overwrite":
            return SyncMethod.OVERWRITE.value
        else:
            # 默认使用增量同步
            logger.warning(f"未知的同步方式: {method_str}，使用默认增量同步")
            return SyncMethod.INCREMENTAL.value

    def _parse_recursion_speed(self, speed_value: int) -> RecursionSpeed:
        """解析递归速度
        
        Args:
            speed_value: 速度值（0-2）
            
        Returns:
            RecursionSpeed: 递归速度枚举
        """
        if speed_value == 1:
            return RecursionSpeed.SLOW
        elif speed_value == 2:
            return RecursionSpeed.FAST
        else:
            # 默认使用正常速度
            return RecursionSpeed.NORMAL

    async def perform_sync(self, sync_config: GetSyncConfigDetail) -> Dict[str, Any]:
        """执行同步任务
        
        Args:
            sync_config: 同步配置
            
        Returns:
            Dict[str, Any]: 同步结果
        """
        start_time = time.time()
        logger.info(f"开始执行同步任务: {sync_config.id} - {sync_config.remark or '未命名任务'}")
        
        account_schema: Optional[GetDriveAccountDetail] = None
        try:
            from backend.database.db import async_db_session
            from backend.app.coulddrive.crud.crud_drive_account import drive_account_dao
            
            logger.info(f"尝试根据user_id={sync_config.user_id}从数据库获取账号")
            async with async_db_session() as db:
                account_schema = await drive_account_dao.get(db, sync_config.user_id)
                
                if not account_schema:
                    error_msg = f"未找到ID为{sync_config.user_id}的账号，无法执行同步任务"
                    logger.error(error_msg)
                    return {
                        "success": False,
                        "error": error_msg,
                        "elapsed_time": time.time() - start_time
                    }
                
                logger.info(f"成功获取到账号: {account_schema.username or account_schema.user_id} (ID: {account_schema.id})")
        except Exception as e:
            error_msg = f"获取账号时发生错误: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "success": False,
                "error": error_msg,
                "elapsed_time": time.time() - start_time
            }
        
        # 验证账号和配置关系
        if sync_config.user_id != account_schema.id:
            error_msg = f"严重的内部错误: 同步配置 {sync_config.id} 的账号ID({sync_config.user_id})与获取到的账号ID({account_schema.id})不匹配"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "elapsed_time": time.time() - start_time
            }
        
        # 验证账号参数
        if not hasattr(account_schema, "cookies") or not account_schema.cookies:
            error_msg = f"账号 {account_schema.id} 缺少cookies字段，无法执行同步"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "elapsed_time": time.time() - start_time
            }
        
        # 验证账号类型
        if not hasattr(account_schema, "type") or not account_schema.type:
            error_msg = f"账号 {account_schema.id} 缺少type字段，无法确定网盘类型"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "elapsed_time": time.time() - start_time
            }
        
        # 获取全局网盘管理器
        drive_manager = get_drive_manager()
        
        try:
            # 解析源信息
            src_meta = {}
            if sync_config.src_meta:
                try:
                    src_meta = json.loads(sync_config.src_meta)
                except json.JSONDecodeError:
                    logger.warning(f"解析源元数据失败: {sync_config.src_meta}")
            
            logger.info(f"🔍 [调试] 源元数据: {src_meta}")
            
            # 解析目标信息
            dst_meta = {}
            if sync_config.dst_meta:
                try:
                    dst_meta = json.loads(sync_config.dst_meta)
                except json.JSONDecodeError:
                    logger.warning(f"解析目标元数据失败: {sync_config.dst_meta}")
            
            logger.info(f"🔍 [调试] 目标元数据: {dst_meta}")
            logger.info(f"🔍 [调试] 源路径: {sync_config.src_path}")
            # 解析排除和重命名规则
            exclude_rules = None
            if sync_config.exclude:
                try:
                    exclude_rules = json.loads(sync_config.exclude)
                except json.JSONDecodeError:
                    logger.warning(f"解析排除规则失败: {sync_config.exclude}")
            
            rename_rules = None
            if sync_config.rename:
                try:
                    rename_rules = json.loads(sync_config.rename)
                except json.JSONDecodeError:
                    logger.warning(f"解析重命名规则失败: {sync_config.rename}")
            
            # 解析同步方式和递归速度
            sync_method = self._parse_sync_method(sync_config.method.value if hasattr(sync_config.method, 'value') else str(sync_config.method))
            recursion_speed = self._parse_recursion_speed(sync_config.speed)
            
            # 构建源定义
            source_definition = ShareSourceDefinition(
                source_type=src_meta.get("source_type", "friend"),
                source_id=src_meta.get("source_id", ""),
                file_path=sync_config.src_path,
                ext_params=src_meta.get("ext_params", {})
            )
            
            # 构建目标定义
            target_definition = DiskTargetDefinition(
                file_path=sync_config.dst_path,
                file_id=dst_meta.get("file_id", "")
            )
            
            # 获取网盘类型字符串
            if isinstance(sync_config.type, DriveType):
                drive_type_str = sync_config.type.value
            else:
                # 如果是字符串，直接使用
                drive_type_str = sync_config.type
            
            # 执行比较逻辑
            comparison_result = await perform_comparison_logic(
                drive_manager=drive_manager,
                x_token=account_schema.cookies,
                source_definition=source_definition,
                target_definition=target_definition,
                recursive=True,  # 始终递归处理
                recursion_speed=recursion_speed,
                comparison_mode=sync_method,
                exclude_rules_def=exclude_rules,
                rename_rules_def=rename_rules,
                drive_type_str=drive_type_str
            )
            
            # 应用比较结果
            operation_results = await apply_comparison_operations(
                drive_manager=drive_manager,
                x_token=account_schema.cookies,
                comparison_result=comparison_result,
                drive_type_str=drive_type_str
            )
            
            # 计算统计数据
            stats = {
                "added_success": len(operation_results.get("add", {}).get("succeeded", [])),
                "added_fail": len(operation_results.get("add", {}).get("failed", [])),
                "deleted_success": len(operation_results.get("delete", {}).get("succeeded", [])),
                "deleted_fail": len(operation_results.get("delete", {}).get("failed", [])),
                "to_add_total": len(comparison_result.to_add),
                "to_delete_total": len(comparison_result.to_delete_from_target),
                "source_list_num": comparison_result.source_list_num,
                "target_list_num": comparison_result.target_list_num,
                "sync_method": sync_method,
                "recursion_speed": recursion_speed.value
            }
            
            elapsed_time = time.time() - start_time
            logger.info(f"同步任务完成: ID={sync_config.id}, 耗时={elapsed_time:.2f}秒")
            
            return {
                "success": True,
                "stats": stats,
                "details": operation_results,
                "elapsed_time": elapsed_time
            }
            
        except Exception as e:
            error_msg = f"同步任务执行失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "success": False,
                "error": error_msg,
                "elapsed_time": time.time() - start_time
            }

    async def execute_sync_by_config_id(self, config_id: int, db: AsyncSession) -> Dict[str, Any]:
        """根据配置ID执行同步任务"""
        from backend.app.coulddrive.crud.crud_filesync import sync_config_dao
        
        # 使用 CRUD 层的验证方法
        sync_config, error_msg = await sync_config_dao.get_with_validation(db, config_id)
        if not sync_config:
            return {"success": False, "error": error_msg}
        
        if error_msg:  # 配置存在但被禁用
            return {"success": False, "error": error_msg}
        
        # 内联转换数据库模型到详情 Schema
        def get_drive_type_from_db_value(db_value: str) -> DriveType:
            """从数据库值获取 DriveType 枚举"""
            try:
                return DriveType[db_value]
            except KeyError:
                for drive_type in DriveType:
                    if drive_type.value == db_value:
                        return drive_type
                raise ValueError(f"无效的网盘类型: {db_value}，支持的类型: {[dt.value for dt in DriveType]}")
        
        # 使用字典方式创建 schema 对象，确保 field_validator 生效
        try:
            # 将 SQLAlchemy 对象转换为字典，触发 field_validator
            sync_config_dict = {
                'id': sync_config.id,
                'enable': sync_config.enable,
                'remark': sync_config.remark,
                'type': sync_config.type,  # 让 field_validator 处理类型转换
                'src_path': sync_config.src_path,
                'src_meta': sync_config.src_meta,
                'dst_path': sync_config.dst_path,
                'dst_meta': sync_config.dst_meta,
                'user_id': sync_config.user_id,
                'cron': sync_config.cron,
                'speed': sync_config.speed,
                'method': sync_config.method,  # 让 field_validator 处理类型转换
                'end_time': sync_config.end_time,
                'exclude': sync_config.exclude,
                'rename': sync_config.rename,
                'last_sync': sync_config.last_sync,
                'created_time': sync_config.created_time,
                'updated_time': sync_config.updated_time or sync_config.created_time,
                'created_by': getattr(sync_config, 'created_by', 1),
                'updated_by': getattr(sync_config, 'updated_by', 1)
            }
            sync_config_detail = GetSyncConfigDetail.model_validate(sync_config_dict)
        except Exception as e:
            # 如果直接转换失败，使用手动映射
            logger.warning(f"直接转换失败，使用手动映射: {e}")
            sync_config_detail = GetSyncConfigDetail(
                id=sync_config.id,
                enable=sync_config.enable,
                remark=sync_config.remark,
                type=get_drive_type_from_db_value(sync_config.type),
                src_path=sync_config.src_path,
                src_meta=sync_config.src_meta,
                dst_path=sync_config.dst_path,
                dst_meta=sync_config.dst_meta,
                user_id=sync_config.user_id,
                cron=sync_config.cron,
                speed=sync_config.speed,
                method=SyncMethod(sync_config.method) if hasattr(SyncMethod, sync_config.method.upper()) else SyncMethod.INCREMENTAL,
                end_time=sync_config.end_time,
                exclude=sync_config.exclude,
                rename=sync_config.rename,
                last_sync=sync_config.last_sync,
                created_time=sync_config.created_time,
                updated_time=sync_config.updated_time or sync_config.created_time,
                created_by=getattr(sync_config, 'created_by', 1),
                updated_by=getattr(sync_config, 'updated_by', 1)
            )
        
        # 执行同步任务
        return await self.perform_sync(sync_config_detail)

# 创建服务单例
file_sync_service = FileSyncService()

# 以下是文件比较和同步相关的类和函数

class ExclusionRule:
    def __init__(self,
                 pattern: str,
                 target: MatchTarget = MatchTarget.NAME,
                 item_type: ItemType = ItemType.ANY,
                 mode: MatchMode = MatchMode.CONTAINS,
                 case_sensitive: bool = False):
        self.pattern_str = pattern
        self.target = target
        self.item_type = item_type
        self.mode = mode
        self.case_sensitive = case_sensitive

        if not case_sensitive:
            self.pattern_str = self.pattern_str.lower()

        self._compiled_regex: Optional[Pattern] = None
        if self.mode == MatchMode.REGEX:
            try:
                self._compiled_regex = re.compile(self.pattern_str, 0 if self.case_sensitive else re.IGNORECASE)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{self.pattern_str}': {e}")
        elif self.mode == MatchMode.WILDCARD:
            # Convert wildcard to regex
            # Basic conversion: escape regex chars, then replace * with .* and ? with .
            regex_pattern = re.escape(self.pattern_str).replace(r'\*', '.*').replace(r'\?', '.')
            self._compiled_regex = re.compile(regex_pattern, 0 if self.case_sensitive else re.IGNORECASE)


    def _get_value_to_match(self, item: BaseFileInfo) -> Optional[str]:
        value: Optional[str] = None
        if self.target == MatchTarget.NAME:
            value = item.file_name
        elif self.target == MatchTarget.PATH:
            value = item.file_path
        elif self.target == MatchTarget.EXTENSION:
            if not item.is_folder and '.' in item.file_name:
                value = item.file_name.rsplit('.', 1)[-1]
            else: # Folders or files without extension
                return None # Cannot match extension

        if value is not None and not self.case_sensitive:
            return value.lower()
        return value

    def matches(self, item: BaseFileInfo) -> bool:
        # 1. Check item type
        if self.item_type == ItemType.FILE and item.is_folder:
            return False
        if self.item_type == ItemType.FOLDER and not item.is_folder:
            return False

        # 2. Get value to match based on target
        value_to_match = self._get_value_to_match(item)
        if value_to_match is None and self.target == MatchTarget.EXTENSION: # e.g. folder when matching extension
             return False # Cannot match if target value is not applicable
        if value_to_match is None: # Should ideally not happen for NAME/PATH if item is valid
            return False


        # 3. Perform match based on mode
        if self.mode == MatchMode.EXACT:
            return value_to_match == self.pattern_str
        elif self.mode == MatchMode.CONTAINS:
            return self.pattern_str in value_to_match
        elif self.mode == MatchMode.REGEX or self.mode == MatchMode.WILDCARD:
            if self._compiled_regex:
                return bool(self._compiled_regex.search(value_to_match))
            return False # Should not happen if constructor worked for these modes

        return False

class ItemFilter:
    def __init__(self, exclusion_rules: Optional[List[ExclusionRule]] = None):
        self.exclusion_rules: List[ExclusionRule] = exclusion_rules or []

    def add_rule(self, rule: ExclusionRule):
        self.exclusion_rules.append(rule)

    def should_exclude(self, item: BaseFileInfo) -> bool:
        if not self.exclusion_rules:
            return False
        for rule in self.exclusion_rules:
            if rule.matches(item):
                return True
        return False

class RenameRule:
    def __init__(self,
                 match_regex: str,
                 replace_string: str,
                 target_scope: MatchTarget = MatchTarget.NAME, # NAME or PATH
                 case_sensitive: bool = False):
        self.match_regex_str = match_regex
        self.replace_string = replace_string # For re.sub()
        
        if target_scope not in [MatchTarget.NAME, MatchTarget.PATH]:
            raise ValueError("RenameRule target_scope must be MatchTarget.NAME or MatchTarget.PATH")
        self.target_scope = target_scope
        self.case_sensitive = case_sensitive
        
        try:
            self.compiled_regex = re.compile(
                self.match_regex_str, 0 if self.case_sensitive else re.IGNORECASE
            )
        except re.error as e:
            raise ValueError(f"Invalid regex pattern '{self.match_regex_str}' in RenameRule: {e}")

    def generate_new_path(self, item: BaseFileInfo) -> Optional[str]:
        """
        Applies the rename rule to an item and returns the new potential full path.
        Returns None if the rule doesn't change the relevant part or scope is not applicable.
        """
        original_path = item.file_path
        original_name = item.file_name

        if self.target_scope == MatchTarget.NAME:
            new_name = self.compiled_regex.sub(self.replace_string, original_name)
            if new_name == original_name:
                return None # No change in name

            # Reconstruct the full path if name changed
            if original_path == original_name: # Item is at root, path is just its name
                return new_name.replace("\\", "/") 
            
            try:
                # Use PurePosixPath for robust parent path detection and joining
                # Assumes item.file_path is in POSIX format or convertible
                path_obj = PurePosixPath(original_path)
                base_path = path_obj.parent
                # str(base_path) might be '.' if original_path has no directory part (e.g. "file.txt")
                # In such a case, new_path should just be new_name.
                if str(base_path) == "." and not '/' in original_path:
                    return new_name.replace("\\", "/")
                return str(base_path / new_name).replace("\\", "/")
            except Exception:
                 # Fallback for any path manipulation issue (should be rare with PurePosixPath)
                if original_path.endswith(original_name):
                    base_path_str = original_path[:-len(original_name)]
                    if not base_path_str and original_path != original_name: 
                        return new_name.replace("\\", "/")
                    # Ensure base_path_str ends with a slash if it's not empty and not already ending with slash
                    if base_path_str and not base_path_str.endswith('/'):
                         base_path_str += '/'
                    return (base_path_str + new_name).replace("\\", "/")
                return None # Cannot reliably determine base path

        elif self.target_scope == MatchTarget.PATH:
            new_path = self.compiled_regex.sub(self.replace_string, original_path)
            if new_path == original_path:
                return None # No change in path
            return new_path.replace("\\", "/")
        
        return None # Should not be reached if target_scope is validated

def compare_drive_lists(
    source_list: List[BaseFileInfo],
    target_list: List[BaseFileInfo],
    mode: str = "incremental",  
    rename_rules: Optional[List[RenameRule]] = None,
    source_base_path: str = "",  # 源目录基础路径参数
    target_base_path: str = "",  # 目标目录基础路径参数
) -> Dict[str, Any]: 
    """
    比较两个文件列表，识别添加、更新、删除和重命名操作
    
    :param source_list: 源目录文件列表
    :param target_list: 目标目录文件列表
    :param mode: 比较模式，"incremental" 或 "full_sync"
    :param rename_rules: 重命名规则列表
    :param source_base_path: 源目录的基础路径，用于计算相对路径
    :param target_base_path: 目标目录的基础路径，用于计算相对路径
    :return: 比较结果字典，包含 to_add, to_update_in_target, to_delete_from_target, to_rename_in_target 字段
    """
    def get_relative_path(full_path: str, base_path: str) -> str:
        """获取相对路径"""
        if not base_path:
            return full_path
        # 确保路径以/开头
        full_path = full_path if full_path.startswith('/') else '/' + full_path
        base_path = base_path if base_path.startswith('/') else '/' + base_path
        # 移除结尾的/
        base_path = base_path.rstrip('/')
        if full_path.startswith(base_path):
            return full_path[len(base_path):]
        return full_path

    def calculate_target_path_and_parent(source_item: BaseFileInfo) -> Tuple[str, str]:
        """
        计算源文件在目标位置的完整路径和父目录路径
        
        :param source_item: 源文件信息
        :return: (目标完整路径, 目标父目录路径)
        """
        # 计算相对于源基础路径的相对路径
        relative_path_to_source_base = ""
        try:
            if source_item.file_path == source_base_path or not source_item.file_path.startswith(source_base_path):
                if source_item.file_path == source_base_path and source_base_path != "/":
                    relative_path_to_source_base = os.path.basename(source_base_path)
                elif source_item.file_path.startswith(source_base_path) and len(source_item.file_path) > len(source_base_path):
                    relative_path_to_source_base = source_item.file_path[len(source_base_path):].lstrip('/')
                else:
                    relative_path_to_source_base = source_item.file_name
            else:
                relative_path_to_source_base = os.path.relpath(source_item.file_path, start=source_base_path)
        except ValueError:
            relative_path_to_source_base = source_item.file_name
        
        # 构建目标完整路径
        target_full_path = os.path.join(target_base_path, relative_path_to_source_base)
        target_full_path = os.path.normpath(target_full_path).replace("\\", "/")
        
        # 计算父目录路径
        if source_item.is_folder:
            # 对于文件夹，父目录就是其上级目录
            target_parent_path = os.path.dirname(target_full_path).replace("\\", "/")
        else:
            # 对于文件，父目录就是其所在目录
            target_parent_path = os.path.dirname(target_full_path).replace("\\", "/")
        
        return target_full_path, target_parent_path

    # 规范化基础路径
    source_base_path = source_base_path.rstrip('/')
    target_base_path = target_base_path.rstrip('/')

    # 构建目标路径到file_id的映射
    target_path_to_file_id = {}
    for target_item in target_list:
        if target_item.file_path and target_item.file_id:
            target_path_to_file_id[target_item.file_path] = target_item.file_id

    results: Dict[str, List[Any]] = {
        "to_add": [],
        "to_update_in_target": [],
        "to_delete_from_target": [],
        "to_rename_in_target": []
    }

    # 创建相对路径映射
    source_map_by_rel_path: Dict[str, BaseFileInfo] = {
        get_relative_path(item.file_path, source_base_path): item 
        for item in source_list
    }
    target_map_by_rel_path: Dict[str, BaseFileInfo] = {
        get_relative_path(item.file_path, target_base_path): item 
        for item in target_list
    }

    accounted_source_paths: Set[str] = set()
    accounted_target_paths: Set[str] = set()

    # 1. First Pass: Exact path matches (for updates)
    for src_rel_path, src_item in source_map_by_rel_path.items():
        if src_rel_path in target_map_by_rel_path:
            target_item = target_map_by_rel_path[src_rel_path]
            
            is_different = False
            if src_item.is_folder != target_item.is_folder:
                is_different = True
            elif not src_item.is_folder: # If they are both files, compare size
                if src_item.file_size != target_item.file_size:
                    is_different = True

            if is_different:
                results["to_update_in_target"].append({"source": src_item, "target": target_item})
            
            accounted_source_paths.add(src_rel_path)
            accounted_target_paths.add(src_rel_path)

    # 2. Second Pass: Rename detection (using remaining unaccounted items)
    if rename_rules:
        unaccounted_src_items = [(p, i) for p, i in source_map_by_rel_path.items() if p not in accounted_source_paths]
        unaccounted_tgt_items = [(p, i) for p, i in target_map_by_rel_path.items() if p not in accounted_target_paths]
        

        for src_rel_path, src_item in unaccounted_src_items:
            if src_rel_path in accounted_source_paths:
                continue
            
            found_rename_for_current_source = False
            for target_rel_path, target_item in unaccounted_tgt_items:
                if target_rel_path in accounted_target_paths:
                    continue

                # Basic compatibility check (type and size for files)
                if src_item.is_folder == target_item.is_folder and \
                   (src_item.is_folder or src_item.file_size == target_item.file_size):
                    
                    for rule in rename_rules:
                        suggested_new_path = rule.generate_new_path(target_item)
                        if suggested_new_path and suggested_new_path == src_item.file_path:
                            results["to_rename_in_target"].append({
                                'target_item': target_item,
                                'suggested_new_path': src_item.file_path,
                                'source_item': src_item,
                                'applied_rule_pattern': rule.match_regex_str
                            })
                            accounted_source_paths.add(src_rel_path)
                            accounted_target_paths.add(target_rel_path)
                            found_rename_for_current_source = True
                            break
                
                if found_rename_for_current_source:
                    break

    # 3. Third Pass: Remaining items are true adds/deletes
    for src_rel_path, src_item in source_map_by_rel_path.items():
        if src_rel_path not in accounted_source_paths:
            # 计算目标路径信息
            target_full_path, target_parent_path = calculate_target_path_and_parent(src_item)
            
            # 查找目标父目录的file_id
            target_parent_file_id = target_path_to_file_id.get(target_parent_path)
            
            # 如果找不到父目录的file_id，尝试向上查找最近的已存在目录
            if not target_parent_file_id:
                # 从目标父目录开始，逐级向上查找已存在的目录
                current_path = target_parent_path
                while current_path and current_path != "/" and current_path != ".":
                    if current_path in target_path_to_file_id:
                        target_parent_file_id = target_path_to_file_id[current_path]
                        break
                    # 向上一级目录
                    current_path = os.path.dirname(current_path).replace("\\", "/")
                
                # 如果还是找不到，使用根目录（target_base_path）的file_id
                if not target_parent_file_id and target_base_path in target_path_to_file_id:
                    target_parent_file_id = target_path_to_file_id[target_base_path]
                
                # 如果仍然找不到file_id，标记为错误
                if not target_parent_file_id:
                    logger.warning(f"无法找到目标父目录的file_id: {target_parent_path}，将在传输时报错")
            
            # 构建增强的添加项信息
            add_item = {
                "source_item": src_item,
                "target_full_path": target_full_path,
                "target_parent_path": target_parent_path,
                "target_parent_file_id": target_parent_file_id
            }
            results["to_add"].append(add_item)

    if mode == "full_sync":
        for target_rel_path, target_item in target_map_by_rel_path.items():
            if target_rel_path not in accounted_target_paths:
                results["to_delete_from_target"].append(target_item)
    
    return results

def _parse_exclusion_rules(rules_def: Optional[List[ExclusionRuleDefinition]]) -> Optional[ItemFilter]:
    if not rules_def:
        return None
    item_filter = ItemFilter()
    for i, rule_data in enumerate(rules_def):
        try:
            item_filter.add_rule(ExclusionRule(
                pattern=rule_data.pattern,
                target=rule_data.target,
                item_type=rule_data.item_type,
                mode=rule_data.mode,
                case_sensitive=rule_data.case_sensitive
            ))
        except ValueError as e:
            # 抛出一个特定的错误，可以被 API 层捕获
            raise ValueError(f"排除规则 #{i+1} ('{rule_data.pattern}') 格式错误: {e}")
    return item_filter

def _parse_rename_rules(rules_def: Optional[List[RenameRuleDefinition]]) -> Optional[List[RenameRule]]:
    if not rules_def:
        return None
    parsed_rules = []
    for i, rule_data in enumerate(rules_def):
        try:
            parsed_rules.append(RenameRule(
                match_regex=rule_data.match_regex,
                replace_string=rule_data.replace_string,
                target_scope=rule_data.target_scope,
                case_sensitive=rule_data.case_sensitive
            ))
        except ValueError as e:
            # Raise a specific error that can be caught by the API layer
            raise ValueError(f"重命名规则 #{i+1} ('{rule_data.match_regex}') 格式错误: {e}")
    return parsed_rules

async def _create_missing_target_directories(
    drive_manager: Any,
    x_token: str,
    to_add: List[Dict[str, Any]],
    target_definition: DiskTargetDefinition,
    drive_type_str: str
) -> None:
    """
    在比较阶段创建缺失的目标目录
    
    :param drive_manager: 网盘管理器实例
    :param x_token: 认证令牌
    :param to_add: 待添加项目列表
    :param target_definition: 目标定义
    :param drive_type_str: 网盘类型字符串
    """
    # 收集所有需要创建的目录路径（只处理target_parent_file_id为None的情况）
    missing_dirs = set()
    for add_item in to_add:
        if not add_item.get("target_parent_file_id"):
            target_parent_path = add_item.get("target_parent_path")
            if target_parent_path and target_parent_path != "/" and target_parent_path != target_definition.file_path:
                missing_dirs.add(target_parent_path)
    
    if not missing_dirs:
        return
    
    # 按路径深度排序，确保先创建父目录
    sorted_dirs = sorted(missing_dirs, key=lambda x: x.count('/'))
    
    # 创建目录并更新to_add中的target_parent_file_id
    created_dir_to_file_id = {}
    
    for dir_path in sorted_dirs:
        try:
            # 找到父目录的file_id
            parent_path = os.path.dirname(dir_path).replace("\\", "/")
            parent_file_id = None
            
            if parent_path == target_definition.file_path:
                # 父目录是根目录
                parent_file_id = target_definition.file_id
            elif parent_path in created_dir_to_file_id:
                # 父目录是刚创建的目录
                parent_file_id = created_dir_to_file_id[parent_path]
            else:
                # 跳过，父目录不存在
                logger.warning(f"无法创建目录 {dir_path}，父目录 {parent_path} 不存在")
                continue
            
            # 获取目录名称
            dir_name = os.path.basename(dir_path)
            
            # 构建 MkdirParam
            from backend.app.coulddrive.schema.file import MkdirParam
            mkdir_params = MkdirParam(
                drive_type=drive_type_str,
                folder_name=dir_name,
                parent_id=parent_file_id
            )
            
            # 创建目录
            new_dir_info = await drive_manager.create_folder(x_token, mkdir_params)
            if new_dir_info and hasattr(new_dir_info, 'file_id'):
                created_dir_to_file_id[dir_path] = new_dir_info.file_id
                logger.info(f"创建目录成功: {dir_path} (file_id: {new_dir_info.file_id})")
            else:
                logger.warning(f"创建目录失败: {dir_path}")
                
        except Exception as e:
            logger.error(f"创建目录 {dir_path} 时发生错误: {e}")
    
    # 更新to_add中的target_parent_file_id
    for add_item in to_add:
        if not add_item.get("target_parent_file_id"):
            target_parent_path = add_item.get("target_parent_path")
            if target_parent_path in created_dir_to_file_id:
                add_item["target_parent_file_id"] = created_dir_to_file_id[target_parent_path]

async def _get_list_for_compare_op(
    drive_manager: Any,
    x_token: str,
    is_source: bool,
    definition: Union[ShareSourceDefinition, DiskTargetDefinition],
    top_level_recursive: bool,
    top_level_recursion_speed: RecursionSpeed,
    item_filter_instance: Optional[ItemFilter],
    drive_type_str: str
) -> Tuple[List[BaseFileInfo], float]:
    """
    获取列表数据用于比较操作
    
    :param drive_manager: 网盘管理器实例
    :param x_token: 认证令牌
    :param is_source: 是否为源端数据
    :param definition: 路径定义（源或目标）
    :param top_level_recursive: 是否递归
    :param top_level_recursion_speed: 递归速度
    :param item_filter_instance: 项目过滤器实例
    :param drive_type_str: 网盘类型字符串
    :return: 文件列表和耗时
    """
    start_time = time.time()
    result_list: List[BaseFileInfo] = []
    
    # 确保异步方法使用 await 调用
    if is_source:
        source_def = definition
        
        # 构建 ListShareFilesParam
        params = ListShareFilesParam(
            drive_type=drive_type_str,
            source_type=source_def.source_type,
            source_id=source_def.source_id,
            file_path=source_def.file_path,
            recursive=top_level_recursive,
            recursion_speed=top_level_recursion_speed
        )
        
        # 使用统一的调用方式
        result_list = await drive_manager.get_share_list(x_token, params)
    else:
        target_def = definition
        
        # 构建 ListFilesParam
        params = ListFilesParam(
            drive_type=drive_type_str,
            file_path=target_def.file_path,
            file_id=target_def.file_id,
            recursive=top_level_recursive,
            recursion_speed=top_level_recursion_speed
        )
        
        # 使用统一的调用方式
        result_list = await drive_manager.get_disk_list(x_token, params)
    
    # 应用过滤器
    if item_filter_instance:
        result_list = [item for item in result_list if not item_filter_instance.should_exclude(item)]
    
    elapsed_time = time.time() - start_time
    return result_list, elapsed_time

async def perform_comparison_logic(
    drive_manager: Any,
    x_token: str,
    source_definition: ShareSourceDefinition,
    target_definition: DiskTargetDefinition,
    recursive: bool,
    recursion_speed: RecursionSpeed,
    comparison_mode: str, 
    exclude_rules_def: Optional[List[ExclusionRuleDefinition]],
    rename_rules_def: Optional[List[RenameRuleDefinition]],
    drive_type_str: str
) -> GetCompareDetail:
    """
    执行比较逻辑
    
    :param drive_manager: 网盘管理器实例
    :param x_token: 认证令牌
    :param source_definition: 源定义
    :param target_definition: 目标定义
    :param recursive: 是否递归
    :param recursion_speed: 递归速度
    :param comparison_mode: 比较模式
    :param exclude_rules_def: 排除规则定义
    :param rename_rules_def: 重命名规则定义
    :param drive_type_str: 网盘类型字符串
    :return: 比较结果详情
    """
    
    common_item_filter = _parse_exclusion_rules(exclude_rules_def)
    
    source_list, source_time = await _get_list_for_compare_op(
        drive_manager=drive_manager,
        x_token=x_token,
        is_source=True,
        definition=source_definition,
        top_level_recursive=recursive,
        top_level_recursion_speed=recursion_speed,
        item_filter_instance=common_item_filter,
        drive_type_str=drive_type_str
    )
    
    target_list, target_time = await _get_list_for_compare_op(
        drive_manager=drive_manager,
        x_token=x_token,
        is_source=False,
        definition=target_definition,
        top_level_recursive=recursive,
        top_level_recursion_speed=recursion_speed,
        item_filter_instance=common_item_filter,
        drive_type_str=drive_type_str
    )
    
    parsed_rename_rules = _parse_rename_rules(rename_rules_def)

    # compare_drive_lists 返回基础的比较结果字典
    comparison_result = compare_drive_lists(
        source_list=source_list,
        target_list=target_list,
        mode=comparison_mode,
        rename_rules=parsed_rename_rules,
        source_base_path=source_definition.file_path,
        target_base_path=target_definition.file_path
    )
    
    # 在比较阶段创建缺失的目标目录
    await _create_missing_target_directories(
        drive_manager=drive_manager,
        x_token=x_token,
        to_add=comparison_result.get('to_add', []),
        target_definition=target_definition,
        drive_type_str=drive_type_str
    )
    
    # 构建完整的 GetCompareDetail 对象所需的数据
    compare_detail_data = {
        "drive_type": drive_type_str,
        "source_list_num": len(source_list),
        "target_list_num": len(target_list),
        "source_list_time": source_time,
        "target_list_time": target_time,
        "source_definition": source_definition,
        "target_definition": target_definition,
        # 添加比较结果的核心字段
        **comparison_result
    }
    
    # 返回 GetCompareDetail 模型实例
    return GetCompareDetail(**compare_detail_data)

async def apply_comparison_operations(
    drive_manager: Any,
    x_token: str,
    comparison_result: GetCompareDetail,
    drive_type_str: str
) -> Dict[str, Dict[str, List[str]]]:
    """
    根据比较结果执行相应的操作（添加、删除、重命名、更新）

    :param drive_manager: 网盘管理器实例
    :param x_token: 认证令牌
    :param comparison_result: 比较结果，包含to_add、to_delete_from_target等操作列表
    :param drive_type_str: 网盘类型字符串
    :return: 各类操作的结果，格式为:
        {
            "add": {"succeeded": [...], "failed": [...]},
            "delete": {"succeeded": [...], "failed": [...]}
        }
    """
    operation_results = {
        "add": {"succeeded": [], "failed": []},
        "delete": {"succeeded": [], "failed": []}
    }

    # 处理添加操作
    if comparison_result.to_add:
        add_results = await _process_add_operations(
            drive_manager=drive_manager,
            x_token=x_token,
            to_add=comparison_result.to_add,
            source_definition=comparison_result.source_definition,
            target_definition=comparison_result.target_definition,
            drive_type_str=drive_type_str
        )
        operation_results["add"] = add_results

    # 处理删除操作
    if comparison_result.to_delete_from_target:
        delete_results = await _process_delete_operations(
            drive_manager=drive_manager,
            x_token=x_token,
            to_delete=comparison_result.to_delete_from_target,
            drive_type_str=drive_type_str
        )
        operation_results["delete"] = delete_results

    return operation_results

async def _process_add_operations(
    drive_manager: Any,
    x_token: str,
    to_add: List[Dict[str, Any]],  # 修改类型，现在是包含完整信息的字典列表
    source_definition: ShareSourceDefinition,
    target_definition: DiskTargetDefinition,
    drive_type_str: str,
    ext_transfer_params: Optional[Dict[str, Any]] = None
) -> Dict[str, List[str]]:
    """
    处理添加操作，包括创建目录和传输文件
    
    :param drive_manager: 网盘管理器实例
    :param x_token: 认证令牌
    :param to_add: 要添加的文件/目录列表，每个元素包含source_item、target_full_path、target_parent_path等信息
    :param source_definition: 源定义
    :param target_definition: 目标定义
    :param drive_type_str: 网盘类型字符串
    :param ext_transfer_params: 额外的传输参数
    :return: 操作结果，包含succeeded和failed两个列表
    """
    operation_results = {'succeeded': [], 'failed': []}

    # 提取source_item进行排序
    sorted_to_add = sorted(to_add, key=lambda add_item: add_item["source_item"].file_path)

    # 按目标父目录分组文件
    files_to_transfer_by_target_parent: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for add_item in sorted_to_add:
        source_item = add_item["source_item"]
        if not source_item.is_folder:
            target_parent_path = add_item["target_parent_path"]
            files_to_transfer_by_target_parent[target_parent_path].append(add_item)
    
    for target_parent_dir, add_items_in_group in files_to_transfer_by_target_parent.items():
        if not add_items_in_group:
            continue

        # 确保目标路径使用正斜杠
        normalized_target_parent_dir = os.path.normpath(target_parent_dir).replace("\\", "/")
        
        try:
            source_fs_ids_to_transfer = [add_item["source_item"].file_id for add_item in add_items_in_group]
            
            current_transfer_ext_params = {}
            if ext_transfer_params:
                current_transfer_ext_params = {**ext_transfer_params}
            

            
            # 直接传递第一个文件的完整file_ext字典
            first_source_item = add_items_in_group[0]["source_item"]
            if hasattr(first_source_item, 'file_ext') and first_source_item.file_ext:
                file_ext = first_source_item.file_ext
                if isinstance(file_ext, dict):
                    # 将file_ext中的所有参数合并到current_transfer_ext_params
                    current_transfer_ext_params.update(file_ext)
                    
                    # 添加分享文件的父目录ID
                    if first_source_item.parent_id:
                        current_transfer_ext_params['share_parent_fid'] = first_source_item.parent_id
            
            # 如果source_definition有ext_params，也一并加入
            if hasattr(source_definition, 'ext_params') and source_definition.ext_params:
                if isinstance(source_definition.ext_params, dict):
                    # 将source_definition.ext_params中的所有参数合并到current_transfer_ext_params
                    # 这些参数会覆盖file_ext中的同名参数
                    current_transfer_ext_params.update(source_definition.ext_params)
            
            # 获取目标目录的file_id（从比较结果中获取）
            target_dir_file_id = None
            
            # 1. 优先使用比较结果中的file_id
            if add_items_in_group:
                target_dir_file_id = add_items_in_group[0].get("target_parent_file_id")
            
            # 2. 如果是根目录，使用target_definition中的file_id
            if not target_dir_file_id and normalized_target_parent_dir == target_definition.file_path:
                target_dir_file_id = target_definition.file_id
            
            # 如果没有file_id，直接报错
            if not target_dir_file_id:
                error_msg = f"无法获取目标目录的file_id: {normalized_target_parent_dir}"
                logger.error(error_msg)
                for add_item in add_items_in_group:
                    source_item = add_item["source_item"]
                    target_path = add_item["target_full_path"]
                    operation_results['failed'].append(f"TRANSFER_ERROR: {source_item.file_path} -> {target_path} - {error_msg}")
                continue
            
            # 构建transfer所需参数
            try:
                # 构建 TransferParam
                transfer_params = TransferParam(
                    drive_type=drive_type_str,
                    source_type=source_definition.source_type,
                    source_id=source_definition.source_id,
                    source_path=source_definition.file_path,
                    target_path=normalized_target_parent_dir,
                    target_id=target_dir_file_id,  # 使用获取到的具体目录file_id
                    file_ids=source_fs_ids_to_transfer,
                    ext=current_transfer_ext_params
                )
                
                # 使用统一架构的transfer方法
                success_count = await drive_manager.transfer_files(x_token, transfer_params)
                
                # 记录成功的传输
                for add_item in add_items_in_group[:success_count]:
                    source_item = add_item["source_item"]
                    target_path = add_item["target_full_path"]
                    operation_results['succeeded'].append(f"TRANSFER_SUCCESS: {source_item.file_path} -> {target_path}")
                
                # 如果有失败的，也记录下来
                if success_count < len(add_items_in_group):
                    for add_item in add_items_in_group[success_count:]:
                        source_item = add_item["source_item"]
                        target_path = add_item["target_full_path"]
                        operation_results['failed'].append(f"TRANSFER_FAIL: {source_item.file_path} -> {target_path}")
            except Exception as ex_transfer:
                # 记录所有文件传输失败
                for add_item in add_items_in_group:
                    source_item = add_item["source_item"]
                    target_path = add_item["target_full_path"]
                    operation_results['failed'].append(f"TRANSFER_ERROR: {source_item.file_path} -> {target_path} - {str(ex_transfer)}")
        except Exception as ex_group:
            # 整组处理出错
            for add_item in add_items_in_group:
                source_item = add_item["source_item"]
                target_path = add_item["target_full_path"]
                operation_results['failed'].append(f"TRANSFER_GROUP_ERROR: {source_item.file_path} -> {target_path} - {str(ex_group)}")
    
    return operation_results

async def _process_delete_operations(
    drive_manager: Any,
    x_token: str,
    to_delete: List[BaseFileInfo],
    drive_type_str: str
) -> Dict[str, List[str]]:
    """
    处理删除操作
    
    :param drive_manager: 网盘管理器实例
    :param x_token: 认证令牌
    :param to_delete: 要删除的文件/目录列表
    :param drive_type_str: 网盘类型字符串
    :return: 操作结果，包含succeeded和failed两个列表
    """
    operation_results = {'succeeded': [], 'failed': []}
    
    # 收集所有要删除的文件路径和ID
    file_paths = []
    file_ids = []
    
    for item in to_delete:
        if item.file_path:
            # 确保路径是以/开头的绝对路径
            path = item.file_path
            if not path.startswith("/"):
                path = "/" + path
            file_paths.append(path)
        if item.file_id:
            file_ids.append(item.file_id)
    
    # 构建 RemoveParam
    try:
        remove_params = RemoveParam(
            drive_type=drive_type_str,
            file_paths=file_paths,
            file_ids=file_ids
        )
        
        result = await drive_manager.remove_files(x_token, remove_params)
        if result:
            for item in to_delete:
                operation_results['succeeded'].append(f"DELETE_SUCCESS: {item.file_path} (ID: {item.file_id})")
        else:
            for item in to_delete:
                operation_results['failed'].append(f"DELETE_FAILED: {item.file_path} (ID: {item.file_id})")
    except Exception as e:
        for item in to_delete:
            operation_results['failed'].append(f"DELETE_ERROR: {item.file_path} (ID: {item.file_id}) - {str(e)}")
    
    return operation_results 