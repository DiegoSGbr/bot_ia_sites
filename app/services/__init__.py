# Camada de serviços: lógica de negócio e integrações (carregamento de sites, APIs, etc.).

from .site_loader import carrega_site

__all__ = ["carrega_site"]
