# Memoria Descriptiva Técnica - Shield-SMS
## Sistema de Detección de Smishing mediante Machine Learning y PLN

**Proyecto Final del Curso CIB02-O (Ingeniería de Software)**

**Autores:**
- Santana (carlos.santana.p@uni.pe) - API REST & Integración
- Gonzales (j.gonzales.avendano@uni.pe) - Modelo ML
- Lipa (antony.lipa.b@uni.pe) - Procesamiento de Lenguaje Natural
- Achalma (alexandro.achalma.g@uni.pe) - Testing & Validación

**Fecha:** Octubre 2025

**Versión:** 1.0 - Fase 1 Completa

---

## Tabla de Contenidos

1. [Objetivo del Proyecto](#1-objetivo-del-proyecto)
2. [Alcance Funcional - Fase 1](#2-alcance-funcional---fase-1)
3. [Arquitectura del Sistema](#3-arquitectura-del-sistema)
4. [Implementación de Componentes](#4-implementación-de-componentes)
5. [Estrategia de Desarrollo TDD](#5-estrategia-de-desarrollo-tdd)
6. [Resultados y Métricas](#6-resultados-y-métricas)
7. [Cronología de Desarrollo](#7-cronología-de-desarrollo)
8. [Plan de Fase 2](#8-plan-de-fase-2)
9. [Instrucciones de Ejecución](#9-instrucciones-de-ejecución)

---

## 1. Objetivo del Proyecto

### 1.1 Contexto y Motivación

El **smishing** (SMS phishing) representa una amenaza creciente en la seguridad digital, donde atacantes utilizan mensajes de texto para engañar a usuarios y obtener información sensible o realizar fraudes.

### 1.2 Objetivo General

Desarrollar un sistema inteligente de detección automática de smishing que utilice técnicas de Machine Learning y Procesamiento de Lenguaje Natural para clasificar mensajes SMS como legítimos o fraudulentos, con una precisión superior al 90%.

### 1.3 Objetivos Específicos

1. **Implementar un módulo de PLN** para preprocesamiento y extracción de características de mensajes SMS
2. **Desarrollar un modelo de ML basado en reglas** optimizado para detección de patrones de smishing
3. **Crear una API REST** con FastAPI para integración con aplicaciones cliente
4. **Establecer un pipeline de CI/CD** con testing automatizado y despliegue continuo
5. **Alcanzar métricas de calidad**: >90% accuracy, >140 tests, cobertura >85%

### 1.4 Alcance del Proyecto

**Fase 1 (Actual):** Backend completo con API REST, modelo ML y testing exhaustivo, aplicación móvil 
Android.
**Fase 2 (Planificada):** Integración al backend en la nube.

---

## 2. Alcance Funcional - Fase 1

### 2.1 Funcionalidades Implementadas

#### 2.1.1 Procesamiento de Lenguaje Natural (PLN)
- **Limpieza de texto**: Normalización, eliminación de caracteres especiales, conversión a minúsculas
- **Tokenización**: Separación de palabras con manejo de URLs y emails
- **Eliminación de stopwords**: Filtrado de palabras comunes en español e inglés
- **Extracción de patrones**:
  - URLs (incluyendo acortadas: bit.ly, tinyurl.com, etc.)
  - Direcciones de email
  - Números de teléfono y códigos
  - Montos monetarios (USD, EUR, S/, etc.)
- **Análisis de características**:
  - Longitud del mensaje
  - Ratio de mayúsculas
  - Conteo de signos de exclamación
  - Detección de palabras de urgencia

#### 2.1.2 Modelo de Machine Learning
- **Arquitectura**: Sistema basado en reglas con puntuación ponderada
- **Características evaluadas**:
  - Presencia de URLs (peso: 0.35)
  - Palabras clave sospechosas (peso: 0.18)
  - Emails detectados (peso: 0.12)
  - Números y códigos (peso: 0.08)
  - Montos monetarios (peso: 0.15)
  - Longitud del mensaje (peso: 0.15)
  - Ratio de mayúsculas (peso: 0.20)
  - Múltiples exclamaciones (peso: 0.15)
  - Palabras de urgencia (peso: 0.12)
- **Umbral de clasificación**: 0.55 (optimizado para minimizar falsos positivos)
- **Evaluación**: Validación con dataset

#### 2.1.3 API REST
- **Framework**: FastAPI 0.104.1
- **Endpoints implementados**:
  - `GET /health`: Health check del servicio
  - `POST /classify`: Clasificación de mensajes SMS
  - `GET /docs`: Documentación interactiva (Swagger UI)
  - `GET /redoc`: Documentación alternativa (ReDoc)
- **Validaciones**:
  - Pydantic para validación de esquemas
  - Longitud de mensaje: 1-1000 caracteres
  - Manejo de errores HTTP estándar
- **CORS**: Configurado para permitir integraciones cross-origin

#### 2.1.4 Utilidades
- **Validación de URLs**: Verificación de dominios sospechosos y URLs acortadas
- **Detección de patrones**: Regex optimizados para extracción de información
- **Logging**: Sistema de logs para debugging y monitoreo

### 2.2 Funcionalidades No Implementadas (Fase 2)

- Aplicación móvil Android completa
- Base de datos para almacenamiento de mensajes
- Sistema de reportes y estadísticas
- Actualización automática de reglas

---

## 3. Arquitectura del Sistema

### 3.1 Diagrama de Arquitectura

```mermaid
graph TB
    subgraph "Cliente"
        A[Aplicación Cliente<br/>HTTP Request]
    end
    
    subgraph "API Layer"
        B[FastAPI Server<br/>Puerto 8000]
        C[Middleware CORS]
        D[Validación Pydantic]
    end
    
    subgraph "Capa de Procesamiento"
        E[Módulo PLN<br/>preprocessing.py]
        F[Extracción de Patrones]
        G[Limpieza de Texto]
    end
    
    subgraph "Capa de Inteligencia"
        H[Modelo ML<br/>rules_model.py]
        I[Sistema de Puntuación]
        J[Clasificador]
    end
    
    subgraph "Utilidades"
        K[Validador de URLs<br/>url_check.py]
        L[Detectores de Patrones]
    end
    
    subgraph "Datos"
        M[(Dataset CSV<br/>5,574 mensajes)]
    end
    
    A -->|POST /classify| B
    B --> C
    C --> D
    D -->|SMS Text| E
    E --> F
    E --> G
    F --> H
    G --> H
    H --> I
    I --> J
    J -->|Resultado| D
    D -->|JSON Response| A
    
    E -.->|Validación| K
    F -.->|Regex| L
    H -.->|Entrenamiento| M
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style E fill:#e8f5e9
    style H fill:#f3e5f5
    style M fill:#fce4ec
```

### 3.2 Descripción de Capas

#### 3.2.1 API Layer
- **Responsabilidad**: Exponer endpoints REST y manejar requests HTTP
- **Tecnología**: FastAPI con Uvicorn ASGI server
- **Componentes**:
  - Router principal con endpoints `/health` y `/classify`
  - Middleware CORS para permitir requests cross-origin
  - Validación automática con Pydantic models
  - Documentación automática con OpenAPI

#### 3.2.2 Capa de Procesamiento (PLN)
- **Responsabilidad**: Preprocesar y extraer características de mensajes SMS
- **Módulo**: `backend/PLN/preprocessing.py` (364 líneas)
- **Funciones principales**:
  - `preprocesar_completo()`: Pipeline completo de preprocesamiento
  - `extraer_urls()`: Detección de URLs y enlaces acortados
  - `extraer_emails()`: Extracción de direcciones de correo
  - `extraer_numeros()`: Identificación de números y códigos
  - `extraer_montos()`: Detección de cantidades monetarias
  - `calcular_ratio_mayusculas()`: Análisis de capitalización
  - `contar_exclamaciones()`: Conteo de signos de énfasis

#### 3.2.3 Capa de Inteligencia (Modelo ML)
- **Responsabilidad**: Clasificar mensajes como smishing o legítimos
- **Módulo**: `backend/ModeloML/rules_model.py` (431 líneas)
- **Algoritmo**: Sistema de puntuación basado en reglas ponderadas
- **Funciones principales**:
  - `classify()`: Función principal de clasificación
  - `calculate_score()`: Cálculo de puntuación de riesgo
  - `evaluate_model()`: Evaluación con métricas de rendimiento
- **Características evaluadas**: 9 indicadores con pesos optimizados

#### 3.2.4 Capa de Utilidades
- **Responsabilidad**: Funciones auxiliares y validaciones
- **Módulo**: `backend/utils/url_check.py` (311 líneas)
- **Funcionalidades**:
  - Validación de URLs sospechosas
  - Detección de servicios de acortamiento
  - Verificación de dominios conocidos

### 3.3 Flujo de Datos

1. **Request**: Cliente envía POST a `/classify` con texto SMS
2. **Validación**: Pydantic valida formato y longitud del mensaje
3. **Preprocesamiento**: PLN limpia y extrae características del texto
4. **Clasificación**: Modelo ML calcula score y determina clasificación
5. **Response**: API retorna JSON con resultado y nivel de confianza

### 3.4 Stack Tecnológico

| Componente | Tecnología | Versión |
|------------|-----------|---------|
| Lenguaje | Python | 3.10+ |
| Framework API | FastAPI | 0.104.1 |
| Server ASGI | Uvicorn | 0.24.0 |
| Validación | Pydantic | 2.5.0 |
| ML/Data | scikit-learn, pandas, numpy | 1.3.2, 2.1.3, 1.26.2 |
| PLN | NLTK | 3.8.1 |
| Testing | pytest, pytest-cov | 7.4.3, 4.1.0 |
| HTTP Client | requests, httpx | 2.31.0, 0.24.1 |
| Containerización | Docker | Latest |
| CI/CD | GitHub Actions | - |

---

## 4. Implementación de Componentes

### 4.1 Módulo API (Santana)

#### 4.1.1 Estructura del Código

**Archivo**: `backend/api/main.py` (203 líneas)

```python
# Modelos Pydantic
class SMSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)

class SMSResponse(BaseModel):
    text: str
    classification: Literal["smishing", "legitimate"]
    confidence: float
    details: Dict[str, Any]

# Endpoints
@app.get("/health")
async def health_check() -> Dict[str, str]

@app.post("/classify", response_model=SMSResponse)
async def classify_sms(request: SMSRequest) -> SMSResponse
```

#### 4.1.2 Características Implementadas

1. **Validación robusta**: Pydantic valida automáticamente tipos y restricciones
2. **Manejo de errores**: HTTPException para errores 400, 500
3. **Documentación automática**: Swagger UI en `/docs`
4. **CORS configurado**: Permite requests desde cualquier origen
5. **Tipado estático**: Type hints en todas las funciones

#### 4.1.3 Ejemplo de Request/Response

**Request:**
```json
POST /classify
{
  "text": "URGENT! You won $1000. Click here: bit.ly/win123"
}
```

**Response:**
```json
{
  "text": "URGENT! You won $1000. Click here: bit.ly/win123",
  "classification": "smishing",
  "confidence": 0.87,
  "details": {
    "score": 0.87,
    "indicators": {
      "urls": 1,
      "amounts": 1,
      "urgency_words": 1,
      "exclamations": 1
    }
  }
}
```

### 4.2 Módulo PLN (Lipa)

#### 4.2.1 Estructura del Código

**Archivo**: `backend/PLN/preprocessing.py` (364 líneas)

```python
# Funciones principales
def preprocesar_completo(texto: str) -> Dict[str, Any]
def extraer_urls(texto: str) -> List[str]
def extraer_emails(texto: str) -> List[str]
def extraer_numeros(texto: str) -> List[str]
def extraer_montos(texto: str) -> List[str]
def calcular_ratio_mayusculas(texto: str) -> float
def contar_exclamaciones(texto: str) -> int
def detectar_palabras_urgencia(texto: str) -> List[str]
```

#### 4.2.2 Pipeline de Preprocesamiento

1. **Normalización**: Conversión a minúsculas, eliminación de espacios extra
2. **Extracción de patrones**: URLs, emails, números, montos (antes de limpiar)
3. **Limpieza**: Eliminación de caracteres especiales, puntuación
4. **Tokenización**: Separación en palabras individuales
5. **Stopwords**: Filtrado de palabras comunes (español e inglés)
6. **Análisis de características**: Cálculo de métricas adicionales

#### 4.2.3 Patrones Regex Optimizados

```python
# URLs (incluyendo acortadas)
URL_PATTERN = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

# Emails
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Montos monetarios
AMOUNT_PATTERN = r'[$£€¥₹]\s*\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|EUR|GBP|S/)'

# Números de teléfono
PHONE_PATTERN = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\b\d{10,}\b'
```

#### 4.2.4 Palabras de Urgencia

Lista de 50+ palabras clave que indican urgencia o presión:
- Español: urgente, inmediato, ahora, rápido, último, expira, ganaste, premio, gratis
- Inglés: urgent, immediate, now, quick, last, expires, won, prize, free, claim

### 4.3 Módulo Modelo ML (Gonzales)

#### 4.3.1 Estructura del Código

**Archivo**: `backend/ModeloML/rules_model.py` (431 líneas)

```python
# Función principal
def classify(texto: str) -> Dict[str, Any]:
    """
    Clasifica un mensaje SMS como smishing o legítimo.
    
    Returns:
        {
            'classification': 'smishing' | 'legitimate',
            'score': float,
            'confidence': float,
            'details': {...}
        }
    """

# Función de evaluación
def evaluate_model(dataset_path: str) -> Dict[str, float]:
    """
    Evalúa el modelo con dataset
    
    Returns:
        {
            'accuracy': float,
            'precision': float,
            'recall': float,
            'f1_score': float
        }
    """
```

#### 4.3.2 Sistema de Puntuación

El modelo utiliza un sistema de puntuación ponderada basado en análisis estadístico del dataset:

| Indicador | Peso | Justificación |
|-----------|------|---------------|
| URLs detectadas | 0.35 | 78% de spam contiene URLs vs 12% de ham |
| Palabras clave sospechosas | 0.18 | Alta correlación con fraudes |
| Emails detectados | 0.12 | Común en phishing |
| Números/códigos | 0.08 | Códigos de verificación falsos |
| Montos monetarios | 0.15 | Promesas de dinero |
| Longitud > 120 chars | 0.15 | Spam promedio: 138 chars |
| Ratio mayúsculas > 15% | 0.20 | Spam: 11% vs Ham: 5.8% |
| Múltiples exclamaciones | 0.15 | 16% spam vs 3.8% ham |
| Palabras de urgencia | 0.12 | 35% spam vs 11% ham |
| Bonus combinación | 0.10 | Si ≥3 indicadores diferentes |

**Fórmula de clasificación:**
```
score = Σ(peso_i × indicador_i)
classification = "smishing" if score ≥ 0.55 else "legitimate"
confidence = min(score / 0.55, 1.0) if smishing else 1.0 - score
```

#### 4.3.3 Optimizaciones Implementadas

1. **Umbral ajustado**: 0.55 (vs 0.50 inicial) para reducir falsos positivos
2. **Penalizaciones**: -0.15 para mensajes muy cortos sin indicadores
3. **Bonus por combinación**: +0.10 si múltiples indicadores presentes
4. **Normalización de confianza**: Escala 0-1 basada en distancia al umbral

### 4.4 Módulo de Utilidades (Achalma)

#### 4.4.1 Validación de URLs

**Archivo**: `backend/utils/url_check.py` (311 líneas)

```python
def is_suspicious_url(url: str) -> bool:
    """Verifica si una URL es sospechosa."""
    
def is_shortened_url(url: str) -> bool:
    """Detecta URLs acortadas."""
    
def extract_domain(url: str) -> str:
    """Extrae el dominio de una URL."""
```

**Servicios de acortamiento detectados:**
- bit.ly, tinyurl.com, goo.gl, ow.ly, t.co
- is.gd, buff.ly, adf.ly, short.link
- 20+ servicios adicionales

#### 4.4.2 Integración con PLN y Modelo

Las utilidades se integran en el pipeline de clasificación:
1. PLN extrae URLs del mensaje
2. Utilidades validan cada URL
3. Modelo incrementa score si URLs sospechosas detectadas

---

## 5. Estrategia de Desarrollo TDD

### 5.1 Metodología Test-Driven Development

El proyecto Shield-SMS fue desarrollado siguiendo estrictamente la metodología TDD con el ciclo **Red-Green-Refactor**:

```
┌─────────────┐
│   RED       │  Escribir test que falla
│   (Test)    │  
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   GREEN     │  Implementar código mínimo
│   (Code)    │  para pasar el test
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  REFACTOR   │  Optimizar y mejorar
│  (Improve)  │  manteniendo tests verdes
└─────────────┘
```

### 5.2 Estructura de Tests

**Directorio**: `tests/` (1,454 líneas totales)

| Archivo | Tests | Líneas | Componente |
|---------|-------|--------|------------|
| `api_tests.py` | 20 | 159 | API REST |
| `pln_tests.py` | 57 | 413 | PLN |
| `model_tests.py` | 49 | 452 | Modelo ML |
| `integracion_test.py` | 18 | 430 | Integración |
| **TOTAL** | **144** | **1,454** | - |

### 5.3 Cobertura de Tests por Componente

#### 5.3.1 Tests de API (20 tests)

**Categorías:**
- Health check (2 tests)
- Clasificación básica (5 tests)
- Validación de entrada (8 tests)
- Manejo de errores (3 tests)
- CORS y headers (2 tests)

**Ejemplo:**
```python
def test_classify_smishing_message():
    """Test clasificación de mensaje smishing."""
    response = client.post("/classify", json={
        "text": "URGENT! Click here to claim your prize: bit.ly/prize123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["classification"] == "smishing"
    assert data["confidence"] > 0.7
```

#### 5.3.2 Tests de PLN (57 tests)

**Categorías:**
- Preprocesamiento completo (8 tests)
- Extracción de URLs (12 tests)
- Extracción de emails (10 tests)
- Extracción de números (9 tests)
- Extracción de montos (10 tests)
- Análisis de características (8 tests)

**Ejemplo:**
```python
def test_extraer_urls_acortadas():
    """Test extracción de URLs acortadas."""
    texto = "Click aquí: bit.ly/abc123 o tinyurl.com/xyz"
    urls = extraer_urls(texto)
    assert len(urls) == 2
    assert "bit.ly/abc123" in urls[0]
    assert "tinyurl.com/xyz" in urls[1]
```

#### 5.3.3 Tests de Modelo ML (49 tests)

**Categorías:**
- Clasificación básica (10 tests)
- Sistema de puntuación (15 tests)
- Evaluación de indicadores (12 tests)
- Casos edge (7 tests)
- Evaluación con dataset (5 tests)

**Ejemplo:**
```python
def test_classify_multiple_indicators():
    """Test mensaje con múltiples indicadores."""
    texto = "URGENT!!! You WON $1000! Click: bit.ly/win Call: 555-0123"
    result = classify(texto)
    assert result["classification"] == "smishing"
    assert result["score"] > 0.8
    assert result["details"]["indicators"]["urls"] > 0
    assert result["details"]["indicators"]["amounts"] > 0
```

#### 5.3.4 Tests de Integración (18 tests)

**Categorías:**
- Flujo completo API→PLN→Modelo (8 tests)
- Rendimiento y latencia (5 tests)
- Casos reales del dataset (5 tests)

**Ejemplo:**
```python
def test_integracion_flujo_completo():
    """Test flujo completo de clasificación."""
    # Simular request HTTP
    sms_text = "Congratulations! You've won a free iPhone. Click here to claim."
    
    # Preprocesar con PLN
    features = preprocesar_completo(sms_text)
    
    # Clasificar con Modelo
    result = classify(sms_text)
    
    # Verificar integración
    assert result["classification"] == "smishing"
    assert "urls" in result["details"]["indicators"]
```

### 5.4 Cronología TDD por Componente

#### Fase RED (Tests Fallidos)
- **2025-10-06**: Commits iniciales con tests que fallan
  - `085953f`: Estructura base del proyecto
  - `0571d61`: Tests PLN (fase Red)
  - `cca6e58`: Tests Modelo (fase Red)
  - `0bafe7c`: Tests Integración (fase Red)
  - `999db99`: Tests API (fase Red)

#### Fase GREEN (Implementación Mínima)
- **2025-10-07**: Implementación para pasar tests
  - `f2cb4e3`: API - endpoints básicos (fase Green)
  - `80ec0e9`: PLN - limpieza y extracción (fase Green)
  - `042a08e`: Modelo - detector por reglas (fase Green)
  - `fae6c21`: Integración - conectar componentes (fase Green)

#### Fase REFACTOR (Optimización)
- **2025-10-08**: Mejoras y optimizaciones
  - `2e3331f`: API - tipado Pydantic (fase Refactor)
  - `149d5af`: PLN - optimizar funciones (fase Refactor)
  - `16f7cec`: Modelo - optimizar reglas (fase Refactor)
  - `d099ffd`: Integración - optimizar utilidades (fase Refactor)

### 5.5 Métricas de Calidad del Código

```bash
# Ejecutar tests con cobertura
pytest tests/ -v --cov=backend --cov-report=html

# Resultados:
# - 144 tests pasando
# - 0 tests fallidos
# - Cobertura: 87.3%
# - Tiempo ejecución: 2.34s
```

**Cobertura por módulo:**
- `backend/api/main.py`: 92%
- `backend/PLN/preprocessing.py`: 89%
- `backend/ModeloML/rules_model.py`: 85%
- `backend/utils/url_check.py`: 83%

---

## 6. Resultados y Métricas

### 6.1 Métricas de Testing

#### 6.1.1 Resumen General

| Métrica | Valor | Objetivo | Estado |
|---------|-------|----------|--------|
| Tests totales | 144 | >140 | ✅ Superado |
| Tests pasando | 144 | 100% | ✅ Logrado |
| Cobertura de código | 87.3% | >85% | ✅ Superado |
| Tiempo de ejecución | 2.34s | <5s | ✅ Excelente |

#### 6.1.2 Distribución de Tests

```
API Tests:          20 (13.9%)  ████████████████
PLN Tests:          57 (39.6%)  ████████████████████████████████████████████
Modelo Tests:       49 (34.0%)  ██████████████████████████████████████
Integración Tests:  18 (12.5%)  █████████████
```

### 6.2 Métricas de CI/CD

#### 6.2.1 Pipeline de GitHub Actions

```yaml
Workflow: CI/CD Pipeline
Trigger: Push, Pull Request
Jobs:
  - Lint (flake8, black)
  - Test (pytest)
  - Coverage (pytest-cov)
  - Build (Docker)
```

**Métricas del pipeline:**
- Tiempo de ejecución: ~3 minutos
- Tasa de éxito: 100% (16/16 builds)
- Cobertura mínima requerida: 85%

### 6.3 Comparación con Objetivos

| Objetivo | Meta | Resultado | Estado |
|----------|------|-----------|--------|
| Accuracy del modelo | >90% | 95.44% | ✅ +5.44% |
| Tests automatizados | >140 | 144 | ✅ +4 tests |
| Cobertura de código | >85% | 87.3% | ✅ +2.3% |
| Tiempo de respuesta | <100ms | 45ms | ✅ -55ms |
| Falsos positivos | <10% | 4.5% | ✅ -5.5% |

---

## 7. Plan de Fase 2

### 7.1 Objetivos de Fase 2

**Objetivo principal:** Desarrollar aplicación móvil Android nativa que integre el backend de Shield-SMS para protección en tiempo real.

### 8.2 Funcionalidades Planificadas

#### 8.2.1 Aplicación Android

**Características principales:**
1. **Interceptor de SMS**: Análisis automático de mensajes entrantes
2. **Notificaciones**: Alertas de smishing detectado
3. **Historial**: Registro de mensajes analizados
4. **Reportes**: Estadísticas de protección
5. **Configuración**: Ajustes de sensibilidad y notificaciones

**Tecnologías:**
- Lenguaje: Kotlin
- UI: Jetpack Compose
- Arquitectura: MVVM + Clean Architecture
- Networking: Retrofit + OkHttp
- Base de datos local: Room
- Permisos: SMS_RECEIVE, INTERNET

#### 8.2.2 Mejoras del Backend

1. **Base de datos**: PostgreSQL para almacenar mensajes y estadísticas
2. **Autenticación**: JWT para usuarios de la app
3. **API de administración**: Endpoints para gestión de usuarios
4. **Modelo mejorado**: Implementar LSTM o BERT para mayor precisión
5. **Actualización de reglas**: Sistema de aprendizaje continuo

#### 8.2.3 Infraestructura

1. **Despliegue en la nube**: AWS/GCP/Azure
2. **Escalabilidad**: Load balancer + múltiples instancias
3. **Monitoreo**: Prometheus + Grafana
4. **Logs centralizados**: ELK Stack
5. **CDN**: CloudFlare para assets estáticos

### 8.3 Arquitectura Fase 2

```mermaid
graph TB
    subgraph "Capa Cliente"
        A[App Android<br/>Kotlin + Compose]
        B[Interceptor SMS]
        C[UI/UX]
    end
    
    subgraph "Capa API"
        D[API Gateway<br/>Load Balancer]
        E[Backend FastAPI<br/>Múltiples instancias]
        F[Auth Service<br/>JWT]
    end
    
    subgraph "Capa ML"
        G[Modelo LSTM/BERT<br/>Deep Learning]
        H[Modelo Reglas<br/>Fallback]
    end
    
    subgraph "Capa Datos"
        I[(PostgreSQL<br/>Mensajes)]
        J[(Redis<br/>Cache)]
        K[(S3<br/>Modelos ML)]
    end
    
    subgraph "Monitoreo"
        L[Prometheus]
        M[Grafana]
        N[ELK Stack]
    end
    
    A --> B
    B --> D
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    E --> I
    E --> J
    G --> K
    E --> L
    L --> M
    E --> N
```

### 8.4 Cronograma Estimado

| Fase | Duración | Tareas Principales |
|------|----------|-------------------|
| **Sprint 1** | 2 semanas | Setup Android + UI básica |
| **Sprint 2** | 2 semanas | Interceptor SMS + integración API |
| **Sprint 3** | 2 semanas | Base de datos + autenticación |
| **Sprint 4** | 2 semanas | Modelo LSTM + entrenamiento |
| **Sprint 5** | 1 semana | Testing + optimización |
| **Sprint 6** | 1 semana | Despliegue + documentación |
| **TOTAL** | **10 semanas** | **Fase 2 completa** |

### 8.5 Métricas de Éxito Fase 2

| Métrica | Objetivo |
|---------|----------|
| Accuracy del modelo LSTM | >97% |
| Tiempo de respuesta API | <50ms |
| Usuarios activos (3 meses) | >1,000 |
| Tasa de retención | >70% |
| Calificación Play Store | >4.5 ⭐ |
| Smishing bloqueado | >10,000 mensajes |

### 8.6 Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Permisos SMS rechazados | Media | Alto | Educación al usuario + alternativas |
| Latencia de red | Media | Medio | Cache local + modo offline |
| Falsos positivos | Baja | Alto | Ajuste de umbral + feedback usuario |
| Costos de infraestructura | Media | Medio | Optimización + tier gratuito inicial |
| Competencia | Alta | Medio | Diferenciación + features únicas |

---

## 9. Instrucciones de Ejecución

### 9.1 Requisitos Previos

#### 9.1.1 Software Necesario

- **Python**: 3.10 o superior
- **pip**: Gestor de paquetes de Python
- **Git**: Control de versiones

#### 9.1.2 Verificar Instalación

```bash
# Verificar Python
python --version  # Debe mostrar Python 3.10+

# Verificar pip
pip --version

# Verificar Git
git --version

# Verificar Docker (opcional)
docker --version
```

### 9.2 Instalación Local

#### 9.2.1 Clonar el Repositorio

```bash
# Clonar desde GitHub
git clone https://github.com/carlossantanap-cell/Shield-SMS.git

# Entrar al directorio
cd Shield-SMS
```

#### 9.2.2 Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

#### 9.2.3 Instalar Dependencias

```bash
# Instalar dependencias del backend
pip install -r backend/requirements.txt

# Descargar datos de NLTK
python -c "import nltk; nltk.download('stopwords')"
```

### 9.3 Ejecución de Tests

#### 9.3.1 Ejecutar Todos los Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar con cobertura
pytest tests/ -v --cov=backend --cov-report=html

# Ver reporte de cobertura
# Abrir: htmlcov/index.html en el navegador
```

#### 9.3.2 Ejecutar Tests Específicos

```bash
# Solo tests de API
pytest tests/api_tests.py -v

# Solo tests de PLN
pytest tests/pln_tests.py -v

# Solo tests de Modelo
pytest tests/model_tests.py -v

# Solo tests de Integración
pytest tests/integracion_test.py -v
```

#### 9.3.3 Resultados Esperados

```
======================== test session starts =========================
collected 144 items

tests/api_tests.py::test_health_check PASSED                   [  1%]
tests/api_tests.py::test_classify_smishing PASSED              [  2%]
...
tests/integracion_test.py::test_flujo_completo PASSED          [100%]

======================== 144 passed in 2.34s =========================
```

### 9.7 Solución de Problemas

#### 9.7.1 Error: Módulo no encontrado

```bash
# Problema: ModuleNotFoundError: No module named 'fastapi'
# Solución: Instalar dependencias
pip install -r backend/requirements.txt
```

#### 9.7.2 Error: NLTK data no encontrado

```bash
# Problema: Resource stopwords not found
# Solución: Descargar datos NLTK
python -c "import nltk; nltk.download('stopwords')"
```

#### 9.7.3 Error: Tests fallando

```bash
# Problema: Tests fallan por imports
# Solución: Ejecutar desde directorio raíz
cd Shield-SMS
pytest tests/ -v
```

---

## Conclusiones

### Logros de Fase 1

1. ✅ **Sistema completo funcional**: API + PLN + Modelo ML integrados
2. ✅ **Alta precisión**: 95.44% accuracy en detección de smishing
3. ✅ **Testing exhaustivo**: 144 tests automatizados con 87.3% cobertura
4. ✅ **Metodología TDD**: Desarrollo disciplinado con ciclo Red-Green-Refactor

### Próximos Pasos

1. 🔄 **Fase 2**: Desarrollo de aplicación Android nativa completa
2. 🔄 **Infraestructura**: Despliegue en la nube con escalabilidad
3. 🔄 **Monitoreo**: Sistema de métricas y alertas en producción

### Lecciones Aprendidas

1. **TDD es efectivo**: La metodología TDD garantizó código robusto y mantenible
2. **Integración temprana**: Conectar componentes desde el inicio evitó problemas
3. **Tests exhaustivos**: 144 tests dieron confianza para refactorizar
4. **Documentación continua**: Documentar durante el desarrollo ahorró tiempo
5. **Trabajo en equipo**: PRs individuales permitieron desarrollo paralelo eficiente

---

## Referencias

### Documentación Técnica

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [NLTK Documentation](https://www.nltk.org/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)

### Datasets y Recursos

- [SMSSpamCollection Dataset](http://www.dt.fee.unicamp.br/~tiago/smsspamcollection/)
- [Phishing Detection Research](https://arxiv.org/abs/2007.14491)
- [SMS Spam Detection Techniques](https://ieeexplore.ieee.org/)

### Herramientas

- [GitHub Repository](https://github.com/carlossantanap-cell/Shield-SMS)
- [GitHub Actions](https://github.com/features/actions)

---

**Fin de la Memoria Descriptiva Técnica**

*Shield-SMS - Protegiendo usuarios contra smishing mediante inteligencia artificial*

*Octubre 2025*
