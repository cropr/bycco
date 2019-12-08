# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from .sv_lang import getLanguageFile
from .sv_page import (
    renderPage, 
    getPage, 
    getPages,
    getPageBySlug,
    getPageBySlugLocale,
    updatePage,
)
from .sv_playerlist import getBelplayer, getFideplayer
from .sv_subscription import (
    getSubscriptions, 
    addSubscription, 
    confirmSubscription,
    getPhoto,
    updatePhoto,
)