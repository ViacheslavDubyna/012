# Встановлення TensorFlow

Цей документ містить інструкції щодо встановлення TensorFlow у вашому середовищі.

## Проблема з довгими шляхами у Windows

При встановленні TensorFlow у вас виникла помилка, пов'язана з довгими шляхами у Windows:

```
ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory: '...'
HINT: This error might have occurred since this system does not have Windows Long Path support enabled.
```

## Вирішення проблеми

### Крок 1: Увімкнення підтримки довгих шляхів у Windows

1. Відкрийте командний рядок або PowerShell від імені адміністратора
2. Виконайте наступну команду:

```
reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v "LongPathsEnabled" /t REG_DWORD /d 1 /f
```

3. Перезавантажте комп'ютер

### Крок 2: Встановлення TensorFlow

Ви можете використати один із двох способів:

#### Спосіб 1: Використання створеного скрипта

1. Запустіть файл `install_tensorflow.py` з правами адміністратора:
   - Відкрийте командний рядок або PowerShell від імені адміністратора
   - Перейдіть до директорії з файлом
   - Виконайте команду: `python install_tensorflow.py`

#### Спосіб 2: Ручне встановлення

1. Відкрийте командний рядок або PowerShell
2. Виконайте наступні команди:

```
python -m pip cache purge
python -m pip uninstall -y tensorflow
python -m pip install tensorflow
```

### Крок 3: Перевірка встановлення

Для перевірки правильності встановлення TensorFlow:

1. Запустіть файл `test_tensorflow.py`:
   - Відкрийте командний рядок або PowerShell
   - Перейдіть до директорії з файлом
   - Виконайте команду: `python test_tensorflow.py`

2. Або в Jupyter Notebook:
   - Перезапустіть ядро Jupyter Notebook
   - Виконайте наступний код:

```python
import tensorflow as tf
print(f"TensorFlow версія: {tf.__version__}")

# Перевірка роботи
a = tf.constant([[1, 2], [3, 4]])
b = tf.constant([[5, 6], [7, 8]])
c = tf.matmul(a, b)
print(f"Результат множення матриць:\n{c}")
```

## Додаткова інформація

- Офіційна документація TensorFlow: [https://www.tensorflow.org/install](https://www.tensorflow.org/install)
- Інформація про проблему з довгими шляхами у Windows: [https://pip.pypa.io/warnings/enable-long-paths](https://pip.pypa.io/warnings/enable-long-paths)