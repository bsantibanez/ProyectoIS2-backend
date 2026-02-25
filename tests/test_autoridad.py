from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def test_flujo_autoridad_completo():
    try:
        # --- LOGIN ---
        driver.get("http://localhost:4200/login")
        driver.maximize_window()
        
        wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys("autoridad@correo.com")
        driver.find_element(By.ID, "password").send_keys("Byron12345")
        driver.find_element(By.ID, "btn-login").click()
        wait.until(EC.presence_of_element_located((By.ID, "admin-panel")))
        print("CP-AU-01 ✅ Login exitoso")

        # --- APROBAR SOLICITUD (CP-AU-02) ---
        btn_aprobar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id, 'btn-aprobar-')]")))
        btn_aprobar.click()   
        for _ in range(2):
            wait.until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        print("CP-AU-02 ✅ Solicitud Aprobada")

        # --- RECHAZAR SOLICITUD (CP-AU-03) ---
        btn_rechazar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id, 'btn-rechazar-')]")))
        btn_rechazar.click()
        for _ in range(2):
            wait.until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        print("CP-AU-03 ✅ Solicitud Rechazada")

        # --- CONSULTAR HISTORIAL (CP-AU-04)---
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.ID, "tab-historial"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "table-historial-admin")))
        print("CP-AU-04 ✅ Historial consultado")

        # --- CIERRE DE SESIÓN (CP-AU-05)---
        btn_logout = wait.until(EC.element_to_be_clickable((By.ID, "btn-logout-admin")))
        btn_logout.click()
        wait.until(EC.alert_is_present())
        alerta_logout = driver.switch_to.alert
        alerta_logout.accept()       
        wait.until(EC.presence_of_element_located((By.ID, "btn-login")))
        
        print("CP-AU-05 ✅ Sesión cerrada y redirección exitosa")

    except Exception as e:
        driver.save_screenshot("error_maestro_autoridad.png")
        print(f"❌ Error en el flujo: {e}")
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    test_flujo_autoridad_completo()