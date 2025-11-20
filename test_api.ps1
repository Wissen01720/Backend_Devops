# Script para probar la API y generar datos en Axiom
# Ejecutar: .\test_api.ps1

$baseUrl = "http://localhost:8000"

Write-Host "🚀 Iniciando pruebas de API..." -ForegroundColor Green
Write-Host ""

# 1. Health Check
Write-Host "1️⃣ Health Check..." -ForegroundColor Cyan
$health = Invoke-RestMethod -Uri "$baseUrl/health"
Write-Host "Respuesta: $($health | ConvertTo-Json)" -ForegroundColor Yellow
Start-Sleep -Seconds 1

# 2. Crear múltiples tareas
Write-Host "`n2️⃣ Creando 10 tareas automáticamente..." -ForegroundColor Cyan

$tareas = @(
    @{title="Implementar autenticación JWT"; description="Agregar seguridad a los endpoints"},
    @{title="Configurar CI/CD en GitHub Actions"; description="Pipeline de despliegue automático"},
    @{title="Optimizar consultas de base de datos"; description="Mejorar rendimiento de queries"},
    @{title="Documentar API en Swagger"; description="Actualizar documentación completa"},
    @{title="Implementar caché con Redis"; description="Reducir carga en la base de datos"},
    @{title="Configurar monitoring con Prometheus"; description="Métricas de performance"},
    @{title="Agregar tests unitarios"; description="Cobertura mínima del 80%"},
    @{title="Migración a Kubernetes"; description="Desplegar en cluster k8s"},
    @{title="Implementar rate limiting"; description="Protección contra abuso"},
    @{title="Backup automático de base de datos"; description="Respaldo diario a S3"}
)

$tareasCreadas = @()

foreach ($tarea in $tareas) {
    $body = $tarea | ConvertTo-Json
    $respuesta = Invoke-RestMethod -Uri "$baseUrl/tasks" -Method POST -Body $body -ContentType "application/json"
    $tareasCreadas += $respuesta
    Write-Host "  ✓ Creada: $($respuesta.title)" -ForegroundColor Green
    Start-Sleep -Milliseconds 500
}

# 3. Listar todas las tareas
Write-Host "`n3️⃣ Obteniendo todas las tareas..." -ForegroundColor Cyan
$todasLasTareas = Invoke-RestMethod -Uri "$baseUrl/tasks"
Write-Host "  Total de tareas: $($todasLasTareas.Count)" -ForegroundColor Yellow

# 4. Actualizar algunas tareas (marcar como completadas)
Write-Host "`n4️⃣ Actualizando tareas (marcando 5 como completadas)..." -ForegroundColor Cyan
for ($i = 0; $i -lt 5; $i++) {
    $taskId = $tareasCreadas[$i].id
    $updateBody = @{completed=$true} | ConvertTo-Json
    $actualizada = Invoke-RestMethod -Uri "$baseUrl/tasks/$taskId" -Method PUT -Body $updateBody -ContentType "application/json"
    Write-Host "  ✓ Completada: $($actualizada.title)" -ForegroundColor Green
    Start-Sleep -Milliseconds 300
}

# 5. Obtener tareas individuales
Write-Host "`n5️⃣ Consultando tareas individuales..." -ForegroundColor Cyan
for ($i = 0; $i -lt 3; $i++) {
    $taskId = $tareasCreadas[$i].id
    $tarea = Invoke-RestMethod -Uri "$baseUrl/tasks/$taskId"
    Write-Host "  → Tarea: $($tarea.title) | Completada: $($tarea.completed)" -ForegroundColor Yellow
    Start-Sleep -Milliseconds 200
}

# 6. Eliminar algunas tareas
Write-Host "`n6️⃣ Eliminando 2 tareas..." -ForegroundColor Cyan
for ($i = 0; $i -lt 2; $i++) {
    $taskId = $tareasCreadas[$i].id
    Invoke-RestMethod -Uri "$baseUrl/tasks/$taskId" -Method DELETE
    Write-Host "  ✗ Eliminada: $($tareasCreadas[$i].title)" -ForegroundColor Red
    Start-Sleep -Milliseconds 300
}

# 7. Verificación final
Write-Host "`n7️⃣ Verificación final..." -ForegroundColor Cyan
$tareasFinales = Invoke-RestMethod -Uri "$baseUrl/tasks"
Write-Host "  Tareas restantes: $($tareasFinales.Count)" -ForegroundColor Yellow

Write-Host "`n✅ Pruebas completadas!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Ve a Axiom para ver todas las trazas:" -ForegroundColor Cyan
Write-Host "   https://app.axiom.co" -ForegroundColor White
Write-Host ""
Write-Host "📝 Resumen de operaciones:" -ForegroundColor Cyan
Write-Host "   • 1 Health check" -ForegroundColor White
Write-Host "   • 10 Tareas creadas (POST)" -ForegroundColor White
Write-Host "   • 2 Consultas de lista (GET /tasks)" -ForegroundColor White
Write-Host "   • 5 Actualizaciones (PUT)" -ForegroundColor White
Write-Host "   • 3 Consultas individuales (GET /tasks/:id)" -ForegroundColor White
Write-Host "   • 2 Eliminaciones (DELETE)" -ForegroundColor White
Write-Host "   Total: ~23 requests con trazas en Axiom" -ForegroundColor Yellow
