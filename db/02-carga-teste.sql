-- Usuários de teste. Não faz parte do software: só serve para exercitar a autenticação.
-- Senhas (apenas para teste): julia = S3nh@-de-teste · kesley = Kesley#2026 · veronica = Veronica!2026
INSERT INTO usuario (id, login, email, nome, hash_senha) VALUES
    ('6f1c2a9e-4b7d-4c3e-9a51-2f0d8e7b1c44', 'julia', 'julia@exemplo.com.br', 'Júlia de Souza Nascimento',
     '$argon2id$v=19$m=19456,t=2,p=1$qXLSXa5k1ePiUeyw/NXpIw$dx3iu71MCivVug9BrsnmOmje3glxm2W2851yT3NrWI4'),
    (DEFAULT, 'kesley', 'kesley@exemplo.com.br', 'Kesley Soares da Silva',
     '$argon2id$v=19$m=19456,t=2,p=1$h0QU8F+bDWqae7axXTLzSA$SFMuQGvMouOssDpgvgZ9rDi9ybCG1PMB9PII/8ANrPo'),
    (DEFAULT, 'veronica', 'veronica@exemplo.com.br', 'Verônica Ribeiro Oliveira Palmeira',
     '$argon2id$v=19$m=19456,t=2,p=1$WWSC4ITrpSlk+e/v+2Eecw$mk4W/dgsit1p0M2cWngF2e9uvLdKUhYq/pyDRqCqE7w');
