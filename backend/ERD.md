```mermaid
erDiagram
    PUNTO_TYPE ||--o{ PUNTO : tiene
    RED_PUNTO ||--o{ PUNTO : tiene
    RED_PUNTO ||--o{ RED : tiene
    USER ||--o{ MULTIPOLIGONO : tiene
    USER ||--o{ RED : tiene
    USER ||--o{ PUNTO : tiene
```