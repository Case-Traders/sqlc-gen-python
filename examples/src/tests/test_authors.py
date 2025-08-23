import os

import pytest
import sqlalchemy.ext.asyncio

from authors import query
from dbtest.migrations import apply_migrations, apply_migrations_async


def test_authors(db: sqlalchemy.engine.Connection):
    apply_migrations(db, [os.path.dirname(__file__) + "/../authors/schema.sql"])

    querier = query.Querier(db)

    authors = list(querier.list_authors())
    assert authors == []

    author_name = "Brian Kernighan"
    author_bio = "Co-author of The C Programming Language and The Go Programming Language"
    new_author = querier.create_author(name=author_name, bio=author_bio)
    assert new_author.id > 0
    assert new_author.name == author_name
    assert new_author.bio == author_bio

    db_author = querier.get_author(id=new_author.id)
    assert db_author == new_author

    author_list = list(querier.list_authors())
    assert len(author_list) == 1
    assert author_list[0] == new_author

    # Test batch insert with copyfrom
    batch_authors = [
        {"p1": "Dennis Ritchie", "p2": "Creator of C Programming Language"},
        {"p1": "Ken Thompson", "p2": "Creator of Unix and Go Programming Language"},
        {"p1": "Rob Pike", "p2": "Co-creator of Go Programming Language"},
    ]
    rows_affected = querier.create_authors_batch(batch_authors)
    assert rows_affected == 3
    
    all_authors = list(querier.list_authors())
    assert len(all_authors) == 4  # 1 existing + 3 batch inserted


@pytest.mark.asyncio
async def test_authors_async(async_db: sqlalchemy.ext.asyncio.AsyncConnection):
    await apply_migrations_async(async_db, [os.path.dirname(__file__) + "/../authors/schema.sql"])

    querier = query.AsyncQuerier(async_db)

    async for _ in querier.list_authors():
        assert False, "No authors should exist"

    author_name = "Brian Kernighan"
    author_bio = "Co-author of The C Programming Language and The Go Programming Language"
    new_author = await querier.create_author(name=author_name, bio=author_bio)
    assert new_author.id > 0
    assert new_author.name == author_name
    assert new_author.bio == author_bio

    db_author = await querier.get_author(id=new_author.id)
    assert db_author == new_author

    author_list = []
    async for author in querier.list_authors():
        author_list.append(author)
    assert len(author_list) == 1
    assert author_list[0] == new_author

    # Test batch insert with copyfrom
    batch_authors = [
        {"p1": "Dennis Ritchie", "p2": "Creator of C Programming Language"},
        {"p1": "Ken Thompson", "p2": "Creator of Unix and Go Programming Language"},
        {"p1": "Rob Pike", "p2": "Co-creator of Go Programming Language"},
    ]
    rows_affected = await querier.create_authors_batch(batch_authors)
    assert rows_affected == 3
    
    all_authors = []
    async for author in querier.list_authors():
        all_authors.append(author)
    assert len(all_authors) == 4  # 1 existing + 3 batch inserted
