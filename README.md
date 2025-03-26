# Mundo Deportivo - Showcase Feed Generator

Este repositorio genera automáticamente un feed compatible con Google Showcase combinando las secciones `/elotromundo/` y `/actualidad/` de Mundo Deportivo.

## ¿Qué hace?

- Descarga y unifica los artículos de dos feeds RSS.
- Recorta títulos a 84 caracteres y resúmenes a 60 caracteres.
- Genera un feed Atom válido con paneles `SINGLE_STORY`.
- Se actualiza automáticamente cada 15 minutos con GitHub Actions.

## ¿Dónde estará disponible?

Una vez subido a GitHub y activado, tu feed estará disponible en:

```
https://cdn.jsdelivr.net/gh/TU_USUARIO/rss-showcase/rss-showcase.xml
```

(Sustituye `TU_USUARIO` por tu nombre de usuario de GitHub)

## Cómo usarlo

1. Crea un nuevo repositorio en GitHub y sube estos archivos.
2. Habilita GitHub Actions (en la pestaña "Actions").
3. ¡Listo! Tu feed se actualizará cada 15 minutos.