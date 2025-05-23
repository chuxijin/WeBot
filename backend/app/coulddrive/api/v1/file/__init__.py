#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.coulddrive.api.v1.file.file import router as file_router

router = APIRouter(prefix='/file')

router.include_router(file_router, tags=['文件管理'])
