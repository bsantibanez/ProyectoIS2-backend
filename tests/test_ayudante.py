from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def ejecutar_flujo_ayudante():
    try:
        # --- LOGIN (CP-AY-01) ---
        driver.get("http://localhost:4200/login")
        driver.maximize_window()
        
        wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys("ayudante@correo.com")
        driver.find_element(By.ID, "password").send_keys("Byron12345")
        driver.find_element(By.ID, "btn-login").click()
        print("CP-AY-01 ✅ Sesión iniciada como Ayudante")

        # --- REGISTRO DE ALUMNO (CP-AY-02) ---
        wait.until(EC.element_to_be_clickable((By.ID, "nav-alumnos"))).click()
        
        rut_test = "21475169-1"
        wait.until(EC.presence_of_element_located((By.ID, "input-alumno-rut"))).send_keys(rut_test)
        driver.find_element(By.ID, "input-alumno-nombre").send_keys("Juan Alberto Pérez")
        driver.find_element(By.ID, "input-alumno-carrera").send_keys("Ingeniería Civil Informática")
        driver.find_element(By.ID, "input-alumno-email").send_keys("juan.perez@correo.com")
        driver.find_element(By.ID, "btn-guardar-alumno").click() 
        
        wait.until(EC.alert_is_present()).accept()
        print(f"CP-AY-02 ✅ Alumno {rut_test} registrado exitosamente")

        # --- CREACIÓN DE SOLICITUDES (CP-AY-03) ---
        for i, motivo in enumerate(["Práctica A", "Práctica B"], 1):
            wait.until(EC.element_to_be_clickable((By.ID, "nav-dashboard"))).click()
            wait.until(EC.presence_of_element_located((By.ID, "input-alumno-rut"))).send_keys(rut_test)
            
            select_element = wait.until(EC.presence_of_element_located((By.ID, "select-recurso-rapido")))
            select = Select(select_element)
            select.select_by_index(i) 
            
            driver.find_element(By.ID, "btn-agregar-recurso").click()
            driver.find_element(By.ID, "input-motivo-solicitud").send_keys(f"{motivo} - Redes Petri")
            driver.find_element(By.ID, "btn-enviar-solicitud").click()
            
            wait.until(EC.alert_is_present()).accept()
            print(f"   - Solicitud {i} generada...")

        print("CP-AY-03 ✅ Solicitudes enviadas a revisión")

        # --- CERRAR SESIÓN (CP-AY-05) ---
        btn_logout = wait.until(EC.element_to_be_clickable((By.ID, "btn-logout")))
        driver.execute_script("arguments[0].scrollIntoView();", btn_logout)
        btn_logout.click()
        btn_login_final = wait.until(EC.presence_of_element_located((By.ID, "btn-login")))
        
        if not btn_login_final.is_enabled():
            print("CP-AY-05 ✅ Flujo finalizado: Usuario fuera del sistema y botón de entrada bloqueado")

    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        driver.save_screenshot("error_ayudante_completo.png")
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    ejecutar_flujo_ayudante()