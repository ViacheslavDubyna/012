# Скрипт для перевірки встановлення TensorFlow

def verify_tensorflow():
    try:
        import tensorflow as tf
        print(f"TensorFlow успішно імпортовано! Версія: {tf.__version__}")
        
        # Виведемо інформацію про доступні пристрої
        print("\nДоступні пристрої:")
        for device in tf.config.list_physical_devices():
            print(f" - {device}")
            
        # Проста операція для перевірки
        print("\nПеревірка роботи TensorFlow:")
        a = tf.constant([[1, 2], [3, 4]])
        b = tf.constant([[5, 6], [7, 8]])
        c = tf.matmul(a, b)
        print(f"Результат множення матриць:\n{c}")
        
        return True
    except ImportError:
        print("Не вдалося імпортувати TensorFlow. Перевірте, чи правильно він встановлений.")
        return False
    except Exception as e:
        print(f"Помилка при перевірці TensorFlow: {e}")
        return False

if __name__ == "__main__":
    print("=== Перевірка встановлення TensorFlow ===")
    verify_tensorflow()
    print("\n=== Завершено ===")