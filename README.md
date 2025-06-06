# INF360-FSW-BackEnd

## Levantar el BackEnd
```uvicorn main:app --reload```

## Instalar dependencias
```pip install -r requirements.txt```

## Documentación
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Arquitectura del BackEnd (Clean Architecture + Modular)
```bash
 INF360-FSW-BackEnd/
│
├── 📁 app/                 # Lógica principal
│   ├── 📁 api/             # Rutas (Endpoints)
│   │   │                 
│   │   ├── 📁 endpoints/
│   │   │   ├── user.py
│   │   │   └── item.py
│   │   ├── router.py        # Incluye y organiza endpoints
│   │   └── deps.py          # Dependencias comunes (auth, db, etc.)
│   │
│   ├── 📁 core/            # Configuración central (CORS, settings)
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── 📁 crud/            # Funciones de acceso a datos (como repositorio)
│   │   └── user.py
│   │
│   ├── 📁 db/ # Base de datos
│   │   ├── base.py          # Declaración base SQLAlchemy
│   │   ├── session.py       # Sesión DB
│   │   └──📁 models/       # Modelos de BD
│   │       └── user.py
│   │
│   ├── 📁 schemas/         # Pydantic models (para entrada/salida)
│   │   ├── user.py
│   │   └── item.py
│   │
│   ├── 📁 services/        # Lógica de negocio
│   │   └── user_service.py
│   │
│   └── main.py              # Punto de entrada de la app
│
├── .env                     # Variables de entorno
├── requirements.txt         # Dependencias
└── launch.json / Dockerfile # Dev tools
```