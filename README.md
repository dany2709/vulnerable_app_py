# vulnerable_app

Mini-proyecto Flask con vulnerabilidades intencionadas:

1. **Hard-coded credentials** en `config.py`.  
2. **SQL Injection** en `/login` (consulta construida con f-string).  
3. **Cross-Site Scripting (XSS)** en `/dashboard` (inserta `{{ user }}` sin escapar).  
4. **Command Injection** en `/ping` (usa `os.popen('ping ' + host)`).  
5. **Code Injection** en `/calc` (eval sobre input).  
6. **Insecure Deserialization** en `/upload` (pickle.load de archivo subido).  
7. **Uso de MD5** en `utils.insecure_hash` (hash débil).  
8. **Debug Mode** activo (`app.run(debug=True)`).

## Instrucciones

```bash
pip install flask
python app.py