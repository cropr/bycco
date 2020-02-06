# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from .sv_account import (
    createAccount,
    deleteAccount,
    getAccount,
    getAccounts,
    loginAccount,
    request2account,
    resetPassword,
    setPassword,
    updateAccount,
    updatePassword,
)
from .sv_lang import getLanguageFile
from .sv_page import (
    renderPage,
    createPage, 
    getPage, 
    getPages,
    getPageBySlug,
    getPageBySlugLocale,
    updatePage,
)
from .sv_doc import (
    renderDoc,
    createDoc, 
    getDoc, 
    getDocBySlug,
    getDocs,
    getLocalizedDoc,
    updateDoc,
)
from .sv_playerlist import getBelplayer, getFideplayer
from .sv_subscription import (
    addSubscription, 
    confirmSubscription,
    csvSubscriptions,
    getPhoto,
    getSubscriptions,
    getSubscription,
    getSubscriptionByIdbel,
    updatePhoto,
)
from .sv_attendee import (
    addAttendee,
    deleteAttendee,
    getAttendee,
    getAttendees,
    getAttendeesCsv,
    updateAttendee,
)
