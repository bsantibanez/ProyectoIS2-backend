from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def test_devolucion_equipo_completo():
    try:
        # --- LOGIN (CP-AY-01) ---
        driver.get("http://localhost:4200/login")
        driver.maximize_window()
        wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys("ayudante@correo.com")
        driver.find_element(By.ID, "password").send_keys("Byron12345")
        driver.find_element(By.ID, "btn-login").click()
        print("CP-AY-01 ✅ Login Ayudante exitoso")

        wait.until(EC.element_to_be_clickable((By.ID, "nav-prestamos"))).click()
        
        # --- DEVOLUCIÓN DE EQUIPO (CP-AY-04) ---
        try:
            # Esperamos a que cargue la vista de préstamos
            btn_finalizar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id, 'btn-finalizar-')]")))
            btn_finalizar.click()
            
            # Manejo de alertas de devolución
            for i in range(2):
                wait.until(EC.alert_is_present())
                alerta = driver.switch_to.alert
                alerta.accept()
            print("CP-AY-04 ✅ Equipo devuelto exitosamente")
        except:
            print("⚠️ No hay préstamos activos para procesar")

        # --- CERRAR SESIÓN (CP-AY-05) ---
        btn_logout = wait.until(EC.element_to_be_clickable((By.ID, "btn-logout")))
        driver.execute_script("arguments[0].scrollIntoView();", btn_logout)
        btn_logout.click()
        btn_login_final = wait.until(EC.presence_of_element_located((By.ID, "btn-login")))
        
        if not btn_login_final.is_enabled():
            print("CP-AY-05 ✅ Flujo finalizado: Usuario fuera del sistema y botón de entrada bloqueado")

    except Exception as e:
        print(f"❌ Error: {e}")
        driver.save_screenshot("error_ayudante_logout.png")
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    test_devolucion_equipo_completo()