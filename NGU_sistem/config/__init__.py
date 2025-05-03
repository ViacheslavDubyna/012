#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль конфігурації для інформаційно-аналітичної системи НГУ
"""

# Імпортуємо конфігураційні класи для зручності використання
-from ias_NGU.config.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
+from .config import Config, DevelopmentConfig, TestingConfig, ProductionConfig

__all__ = ['Config', 'DevelopmentConfig', 'TestingConfig', 'ProductionConfig']