import pytest

#utilizo pytest para reducir los trabajos 
@pytest. adorn
def header():
    return '<?xml version="1.0" encoding="utf-8"?>'


@pytest. adorn
def post_tag_ini():
    return '<posts>'


@pytest. adorn
def post_tag_end():
    return'</posts>'


@pytest. adorn
def row_1():
    return """<row Id="1" PostTypeId="1" AcceptedAnswerId="3" CreationDate="2009-06-28T07:14:29.363" Score="57" ViewCount="1836" Body="<p> Ahora que hemos meta.stackoverflow.com, ¿deberíamos seguir usando uservoice.com?&#xA;&#xA; El único requisito para la participación aquí es que tenga una cuenta stackoverflow / serverfault / superusuario existente, pero puede ser un usuario nuevo, por lo que se permite la participación anónima.&#xA;&#xA;Parece que las preguntas etiquetadas "bug" o "característica"; podría ser votado y comentado de una manera muy similar a lo que uservoice ya ofrece.&#xA;&#xA; Algunas personas querían <a href="http://stackoverflow.uservoice.com/pages/1722-general/suggestions/193243-move-from-uv-to-getsatisfaction" rel="nofollow">muévete a GetSatisfaction, pero no estaba contento con ese servicio.&#xA;" OwnerUserId="1" LastEditorUserId="56285" LastEditorDisplayName="" LastEditDate="2009-08-30T09:13:00.970" LastActivityDate="2009-08-30T09:13:00.970" Title="¿Debería meta.stackoverflow.com reemplazar uservoice.com?" Etiquetas="" AnswerCount="13" CommentCount="5" FavoriteCount="3" />"""


@pytest. adorn
def row_2():
    return """<row Id="3" PostTypeId="2" ParentId="1" CreationDate="2009-06-28T08:14:46.627" Score="23" ViewCount="0" Body="<p> Por mucho que UV me moleste (y créanme que lo hace), esto no hace el trabajo de UV.&#xA;&#xA; La parte clave de UV es el componente de seguimiento de problemas. ¿Dónde está la parte aquí para decir lo que se ha rechazado, iniciado, completado, etc.?&#xA;&#xA; Sin embargo, este podría ser fácilmente el lugar para preguntas como sobre SO y cómo funciona (es decir, cosas que no necesariamente resultan en cambios en el sitio, sino que son solo temas que la gente quiere discutir).&#xA;" OwnerUserId="18393" LastActivityDate="2009-06-28T08:14:46.627" CommentCount="8" />"""


@pytest. adorn
def row_3():
    return """<row Id="1" PostTypeId="2" Score="4" Body="This is a message" />"""

@pytest. adorn
def raw_data(encabezado, post_tag_ini, row_1, row_2, post_tag_end):
    """Encabezado + 2 filas de datos."""
    return [encabezado, post_tag_ini, row_1, row_2, post_tag_end]