### generate_short_id

```
    Gera uma string com caracteres aleatórios que variam entre números e letras.
```

**Parametro**

*num_of_chars*: Número de carateres que teŕá a string gerada

### init_db

```
    Inicializa um banco de dados 'databese.db' com uma tebela de urls, na qual temos a url original (original_url) e o id curto que direciona para ela (short_id)
```

### index

```
    Se for uma requisição POST ele pega a url do formulário, cria um novo short_id e acrescenta essas novas informações ao banco de dados. Se não ele só mostra a página normalmente.
```

