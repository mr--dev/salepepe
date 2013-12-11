CREATE TABLE "categoria" (
    "id_categoria" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "nome" TEXT NOT NULL
);
CREATE TABLE "sezione" (
    "id_sezione" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "nome" TEXT NOT NULL
);
CREATE TABLE ricetta (
    "id_ricetta" INTEGER PRIMARY KEY NOT NULL,
    "numero_rivista" INTEGER,
    "anno_rivista" INTEGER,
    "nome" TEXT,
    "preferito" INTEGER,
    "id_categoria" INTEGER,
    "id_sezione" INTEGER,
    "pagina" TEXT,
    "tags" TEXT
);
