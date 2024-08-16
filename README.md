# Test weatherspotify [WIP] :construction:

## Visão geral
Este serviço sugere playlists musicais com base na temperatura atual de uma cidade especificada. Integrando a API do [OpenWeatherMap](https://openweathermap.org/api) para dados climáticos e a API do [Spotify](https://developer.spotify.com) para sugestões de playlists, o serviço oferece diferentes gêneros musicais conforme a temperatura:
- Se estiver acima de 25°C, o serviço deverá sugerir músicas Pop;
- Se estiver entre 10°C e 25°C, o serviço deverá sugerir músicas de Rock;
- Se estiver abaixo de 10°C, o serviço deverá sugerir músicas clássicas.

## Endpoints da API

*GET* `/login`:
- Descrição: Inicia o fluxo de OAuth com o Spotify. Redireciona o usuário para a página de login do Spotify para autenticação.
- Resposta: Redirecionamento para a página de autorização do Spotify.

*GET* `/callback`:
- Descrição: Manipula o callback do Spotify após o usuário ter se autenticado. Troca o código de autorização por um token de acesso e um token de atualização.
- Parâmetros:
-- code (obrigatório): O código de autorização fornecido pelo Spotify (posteriormente utilizado como 'refresh_token').
-- state (opcional): O valor do estado usado para verificar a solicitação.
- Resposta: Objeto JSON contendo os tokens de acesso e atualização.
- Exemplo de resposta:
```json
{
  "access_token":"BQCjB3B4WHACM2mMl1wtd_mmx_Fb2l3x8OKagzJzZL9tlJ0PXUz1Lu56z_0CZld4ao84u-WhrgVuFWyiQ71s9CpMkfyoDEeXzMviwMLok2xpo9CuOUocRRnpwmgLHh7LBPa1aSw8wPDiM4fG2RTk-mwa-qdul_pVGvf8N0WW5aQTftP3HIAOTvKspD4shrkzftFsXoD-jgTaZ3x9sF0x7Z8XyV0224g",
  "expires_in":3600,
  "refresh_token":"AQAljeFmNHoBeFOQQNkLhxxXPQNodEQ8M7KC0FGGFkp3dz1mLgU7h0wpiOD38Pn7zGEQcaDdwIPaBV2xMK9Q16RQA0_UOMTWQ69hqfrNYVyAehcQi5dIaUZTrkrzuz_24es","scope":"user-read-email user-read-private","token_type":"Bearer"
}
```

*GET* `/playlist`:
- Descrição: Retorna uma playlist sugerida com base na temperatura atual da cidade especificada.
- Parâmetros:
-- city (obrigatório): Nome da cidade para obter a temperatura.
-- refresh_token (obrigatório): Token de atualização do Spotify para obter um novo token de acesso.
- Exemplo de requisiçao: `/playlist?city=Africa&refresh_token=AQAgxZtvsYg5UhrRC2CWhu-9ZH5WUcYjMi2YVsAYjVjcSs`:
- Exemplo de resposta:
```json
{
    "cidade": "Africa",
    "sugestao_playlist": {
        "genero": "rock",
        "tracks": [
            {
                "album": "The Doors",
                "artista": "The Doors",
                "nome": "Light My Fire",
                "url": "https://open.spotify.com/track/5uvosCdMlFdTXhoazkTI5R"
            },
            {
                "album": "Follow The Leader",
                "artista": "Korn",
                "nome": "Freak On a Leash",
                "url": "https://open.spotify.com/track/6W21LNLz9Sw7sUSNWMSHRu"
            },
            {
                "album": "Berry Is On Top",
                "artista": "Chuck Berry",
                "nome": "Johnny B. Goode",
                "url": "https://open.spotify.com/track/4Hbe0lRKsXtDZ2wQIovz7I"
            },
            {
                "album": "After Laughter",
                "artista": "Paramore",
                "nome": "Hard Times",
                "url": "https://open.spotify.com/track/0w5Bdu51Ka25Pf3hojsKHh"
            },
            {
                "album": "Audioslave",
                "artista": "Audioslave",
                "nome": "Like a Stone",
                "url": "https://open.spotify.com/track/2xt2piJx6jlFkjS77YiqpL"
            },
            {
                "album": "Dark Passion Play",
                "artista": "Nightwish",
                "nome": "Amaranth",
                "url": "https://open.spotify.com/track/3CTqSkkNOwV47x8tYj9H7a"
            },
            {
                "album": "Cowboys from Hell",
                "artista": "Pantera",
                "nome": "Cowboys from Hell",
                "url": "https://open.spotify.com/track/2SgbR6ttzoNlCRGQOKjrop"
            },
            {
                "album": "Weezer",
                "artista": "Weezer",
                "nome": "Island In The Sun",
                "url": "https://open.spotify.com/track/2MLHyLy5z5l5YRp7momlgw"
            },
            {
                "album": "From The Fires",
                "artista": "Greta Van Fleet",
                "nome": "Highway Tune",
                "url": "https://open.spotify.com/track/7aOor99o8NNLZYElOXlBG1"
            }
        ]
    },
    "temperatura": "20°C"
}
```

## Tecnologias utilizadas
- Justificativa do Padrão de API
O padrão REST permite que o serviço seja facilmente consumido por diversas aplicações, e foi escolhido pela simplicidade, flexibilidade e ampla adoção na indústria.

- Linguagem e Ferramentas
-- Flask: Um micro framework em Python que oferece simplicidade e rapidez no desenvolvimento de APIs.
-- Python: Escolhido por sua clareza e extensa biblioteca de ferramentas para integração com APIs externas.
-- Requests: Utilizado para fazer requisições HTTP simples e eficientes às APIs do OpenWeatherMap e Spotify.
-- Aiottp: Uma biblioteca para criar servidores HTTP e clientes HTTP assíncronos em Python. É útil para operações de I/O que não bloqueiam o fluxo do programa, melhorando a performance em operações de rede. :construction:

## Decisões arquiteturais:
- Diagrama da arquitetura: [WIP] :construction:

- Latência: :construction:
-- Cache: `Flask-Caching` para armazenar respostas frequentes em `get_weather` e `get_spotify_playlists`. Se houver a necessidade de uma estratégia mais avançada de cache, é considerável utilizar uma ferramenta mais robusta, como o Redis.
Implementar cache dessa forma ajudará a reduzir a latência e a carga nas APIs externas, melhorando a performance geral.

- Resiliência:
-- Tratamento de erros e logs para capturar falhas;
-- Padrões de design como "retry" ou "circuit breaker" para lidar com falhas temporárias. :construction:

- Segurança:
-- Autenticação e autorização e controle de acesso.

- Escalabilidade:
-- Containerização con Docker. :construction:
