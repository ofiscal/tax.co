# How to identify people within a household in the ENPH?


Hi Juan,

Every file in the ENPH starts with these four variables:
    "DIRECTORIO"
    "SECUENCIA_ENCUESTA"
    "SECUENCIA_P"
    "ORDEN"
Their documentation leaves me confused. David told me to interpret DIRECTORIO as household. I believe that's correct (because the number of unique DIRECTORIO values implies an average household size of 3.4 people).

David also said to interpret ORDEN as household member, and that if ORDEN = 1, that's the head of household. So, e.g., if a household has four members, then household member takes values from 1 to 4.

I've discovered that that interpretation cannot be correct.

In Caracteristicas_generales_personas -- which is supposed to be a list of all the people in the survey -- the maximum value of ORDEN is 22. In the purchase files, though, it can be 150. Therefore ORDEN cannot be consistently interpreted as household member. Maybe that's what it means in some files, but definitely not all of them.

In Caracteristicas_generales_personas, SECUENCIA_P is always 1. In other files it can be over 100. Thus, by the same logic, SECUENCIA_P cannot (consistently) mean household member, either.

In Caracteristicas_generales_personas, SECUENCIA_ENCUESTA is always equal to ORDEN (so it also has a maximum value of 22). Its maximum value in the other files is above 1000. Therefore SECUENCIA_ENCUESTA cannot (consistently) mean household member, either.

Do you know anybody at DANE who could clear this up for us?

I've attached a spreadsheet that documents the maximum value of each of those variables. (They all have a minimum of 1.) Anybody helping us might find that useful.

Thanks!
Jeff
