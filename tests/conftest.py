import httpx, pytest
from ai_api_testing.config import settings
from ai_api_testing.schemas import ChatCompletion

@pytest.fixture(scope='session')
def client():
    with httpx.Client(
        base_url=settings.base_url,
        headers={"Authorization": f"Bearer {settings.groq_api_key}"},
        timeout=settings.timeout_seconds
    ) as c:
        yield c

@pytest.fixture(scope='session')
def basic_response(client):
   return client.post("/chat/completions",json={
    "model":settings.model_name,
    "messages":[{"role":"user","content":"Say hello with one word"}],
    "max_tokens":200
   })

@pytest.fixture(scope='session')
def chat(client):
    def _chat(prompt,temperature=0,max_tokens=1000):
        response= client.post("/chat/completions",json={
            "model":settings.model_name,
            "messages":[{"role":"user","content":prompt}],
            "max_tokens":max_tokens,
            "temperature" : temperature
        }) 
        if response.status_code == 429:
            pytest.skip("rate limited (429): inconclusive")
        else:    
            return ChatCompletion.model_validate(response.json()).choices[0].message.content     
    return _chat    

@pytest.fixture(scope='session')
def send(client):
    """Return a callable that sends one chat request and returns the RAW response."""
    def _send(client, user, system=None, temperature=0, max_tokens=1000, **extra):
        messages = []
        if system is not None:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})

        r = client.post("/chat/completions", json={
            "model": settings.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **extra,
        })
        if r.status_code == 429:
            pytest.skip("rate limited (429): inconclusive")
        return r
    return _send
