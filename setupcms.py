import asyncio

from datetime import date, datetime, timedelta, timezone
from bycco import settings
from bycco.crud import get_db

from reddevil.service.sv_page import (
    createPage,
    getPage,
    getRoutingTable,
    updatePage,
)
from reddevil.models.md_page import (
    PageIn,
    PageUpdate,
    PageComponent,
)

from reddevil.models.md_i18nfield import I18nField

async def main():
    """
    prepares the database for testing pages
     - drop the database
     - create an event
     - create 3 members
     - create 2 topics
    """

    # drop database
    print('dropping database')
    db = get_db()
    cl = db.client
    await cl.drop_database('bycco')

    # create page
    page_id = await createPage(PageIn(
        doctype="normal-page",
        name='home',
        locale='nl',
    ))

    # update page
    pu = PageUpdate(
        publicationdate='2020-08-20',
        body= {
            'default': I18nField(id=page_id, name='body', value=''),
            'nl': I18nField(id=page_id, name='body', value=''),
        },
        intro= {
            'default': I18nField(id=page_id, name='intro', value=''),
            'nl': I18nField(id=page_id, name='intro', value=''),
        },
        title= {
            'default': I18nField(id=page_id, name='title', value='Home'),
            'nl': I18nField(id=page_id, name='title', value='Homepagina'),
        },
        component=PageComponent.LandingPage,
    )
    page = await updatePage(page_id, pu)

    # get page
    rt = await getRoutingTable()
    print(f'rt {rt}')

if __name__ == '__main__':
    asyncio.run(main())
