import datetime

from django.db.models import F, Min, Subquery, OuterRef, Sum, Value
from django.shortcuts import render

from blog.models import Blog, ThemeBlog, Entry, EntryDetail, Author, Dog


# Create your views here.


def create_blog(request):
    # SQL INSERT
    b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
    b.save()
    # Equivalent to:
    # Blog.objects.create(name='Beatles Blog', tagline='All the latest Beatles news.')


def save_changes(request):
    # SQL UPDATE
    b = Blog.objects.get(name='Beatles Blog')
    b.name += " Premium"
    b.save()


def save_foreign_field():
    entry = Entry()
    entry.pub_date = datetime.date(2000, 12, 31)
    blog_1 = Blog.objects.get(pk=1)
    entry.blog = blog_1
    entry.save()


def save_many_to_many_field():
    entry = Entry.objects.get(pk=1)
    joe = Author.objects.create(name="Joe")
    entry.authors.add(joe)

    john = Author.objects.create(name="John")
    paul = Author.objects.create(name="Paul")
    entry.authors.add(john, paul)


def retrieve_all_objects():
    Entry.objects.all()


def retrieve_specific_objects_with_filter():
    Entry.objects.filter(pub_date__year=2000)


def exclude_specific_objects_with_exclude():
    Entry.objects.exclude(pub_date__year=2000)


def multiple_filters():
    q1 = Entry.objects.filter(headline__startswith="What")
    q2 = q1.exclude(pub_date__gte=datetime.date.today())
    q3 = q1.filter(pub_date__gte=datetime.date.today())


def chain_multiple_filters():
    Entry.objects.filter(
        headline__startswith='What'
    ).exclude(
        pub_date__gte=datetime.date.today()
    ).filter(
        pub_date__gte=datetime.date(2005, 1, 30)
    )


def lazy_queryset():
    q = Entry.objects.filter(headline__startswith="What")
    q = q.filter(pub_date__lte=datetime.date.today())
    q = q.exclude(body_text__icontains="food")
    print(q)  # Evaluated (database hit)


def retrieve_single_object():
    # You can use any query expression with get(), just like with filter()
    one_entry = Entry.objects.get(pk=1)


def retrieve_single_object_wrongly():
    Entry.objects.get(pk=999)  # raises Entry.DoesNotExist
    Author.objects.get(name__startswith="J")  # raises Author.MultipleObjectsReturned


def limit_queryset():
    # Equivalent of SQL’s LIMIT and OFFSET clauses
    entries = Entry.objects.all()[:5]  # LIMIT 5, not evaluated
    entries = Entry.objects.all()[5:10]  # OFFSET 5 LIMIT 5, not evaluated
    # Negative indexing (i.e. Entry.objects.all()[-1]) is not supported


def step_limit_queryset():
    # Return a list of every second object of the first 10
    Entry.objects.all()[:10:2]  # Evaluated


def retrieve_single_object_index():
    # To retrieve a single object rather than a list (e.g. SELECT foo
    # FROM bar LIMIT 1), use an index instead of a slice.
    Entry.objects.order_by('headline')[0]  # might raise IndexError
    # Roughly equivalent to:
    Entry.objects.order_by('headline')[0:1].get()  # might raise DoesNotExist


def field_lookup_date():
    # Roughly: SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01'
    Entry.objects.filter(pub_date__lte='2006-01-01')


def field_lookup_foreign_key():
    # Roughly: SELECT * FROM blog_entry WHERE blog_id = 1
    Entry.objects.filter(blog_id=1)
    # Equivalent to:
    b = Blog.objects.get(pk=1)
    Entry.objects.filter(blog=b)


def field_lookup_match():
    # Roughly: SELECT * FROM blog_entry WHERE headline = Cat bites dog
    Entry.objects.get(headline__exact="Cat bites dog")
    # Equivalent to:
    Entry.objects.get(headline="Cat bites dog")


def field_lookup_case_insensitive_match():
    # Roughly: SELECT * FROM blog_blog WHERE name LIKE beatles blog'
    Blog.objects.get(name__iexact="beatles blog")


def field_lookup_contains():
    # Roughly: SELECT * FROM blog_entry WHERE headline LIKE %Lennon%
    Entry.objects.get(headline__contains='Lennon')


def field_lookup_case_insensitive_contains():
    # Equivalent to field_lookup_contains() SQL
    Entry.objects.get(headline__icontains='Lennon')


def field_lookup_startswith():
    # Roughly: SELECT * FROM blog_entry WHERE headline LIKE Lennon%
    Entry.objects.get(headline__startswith='Lennon')


def field_lookup_case_insensitive_startswith():
    # Equivalent to field_lookup_startswith() SQL
    Entry.objects.get(headline__istartswith='Lennon')


def field_lookup_endswith():
    # Roughly: SELECT * FROM blog_entry WHERE headline LIKE %Lennon
    Entry.objects.get(headline__endswith='Lennon')


def field_lookup_case_insensitive_endswith():
    # Equivalent to field_lookup_endswith() SQL
    Entry.objects.get(headline__iendswith='Lennon')


def field_lookup_span_relationships():
    # Roughly: SELECT blog_entry.* FROM blog_entry
    # INNER JOIN blog_blog ON (blog_entry.blog_id = blog_blog.id)
    # WHERE blog_blog.name = Beatles Blog
    Entry.objects.filter(blog__name='Beatles Blog')

    # Roughly: SELECT blog_blog.* FROM blog_blog
    # INNER JOIN blog_entry ON (blog_blog.id = blog_entry.blog_id)
    # WHERE blog_entry.headline LIKE %Lennon%
    Blog.objects.filter(entry__headline__contains='Lennon')

    # Roughly: SELECT blog_blog_.* FROM blog_blog
    # INNER JOIN blog_entry ON (blog_blog.id = blog_entry.blog_id)
    # INNER JOIN blog_entry_authors ON (blog_entry.id = blog_entry_authors.entry_id)
    # INNER JOIN blog_author ON (blog_entry_authors.author_id = blog_author.id)
    # WHERE blog_author.name = Lennon
    # If there was no author associated with an entry, it would be treated
    # as if there was also no name attached, rather than raising an error.
    Blog.objects.filter(entry__authors__name='Lennon')

    # Roughly: SELECT blog_blog.* FROM blog_blog
    # LEFT OUTER JOIN blog_entry ON (blog_blog.id = blog_entry.blog_id)
    # LEFT OUTER JOIN blog_entry_authors ON (blog_entry.id = blog_entry_authors.entry_id)
    # LEFT OUTER JOIN blog_author ON (blog_entry_authors.author_id = blog_author.id)
    # WHERE blog_author.name IS NULL
    # Returns Blog objects that have:
    #   an empty name on the author
    #   an empty author on the entry.
    Blog.objects.filter(entry__authors__name__isnull=True)

    # Roughly: SELECT blog_blog.* FROM blog_blog
    # INNER JOIN blog_entry ON (blog_blog.id = blog_entry.blog_id)
    # INNER JOIN blog_entry_authors ON (blog_entry.id = blog_entry_authors.entry_id)
    # INNER JOIN blog_author ON (blog_entry_authors.author_id = blog_author.id)
    # WHERE (blog_entry_authors.author_id IS NOT NULL AND blog_author.name IS NULL)'
    Blog.objects.filter(entry__authors__isnull=False,
                        entry__authors__name__isnull=True)

    # Roughly: SELECT blog_blog.* FROM blog_blog
    # INNER JOIN blog_entry ON (blog_blog.id = blog_entry.blog_id)
    # WHERE (blog_entry.headline LIKE %Lennon% AND
    #        blog_entry.pub_date BETWEEN 2008-01-01 AND 2008-12-31)
    Blog.objects.filter(entry__headline__contains='Lennon',
                        entry__pub_date__year=2008)

    # Roughly: SELECT blog_blog.* FROM blog_blog
    # INNER JOIN blog_entry ON (blog_blog.id = blog_entry.blog_id)
    # INNER JOIN blog_entry T3 ON (blog_blog.id = T3.blog_id)
    # WHERE (blog_entry.headline LIKE %Lennon% AND
    #       T3.pub_date BETWEEN 2008-01-01 AND 2008-12-31)
    # A more permissive query, potentially yielding duplicates.
    Blog.objects.filter(entry__headline__contains='Lennon')\
        .filter(entry__pub_date__year=2008)

    # The behavior of filter() for queries that span multi-value relationships,
    # as described above, is not implemented equivalently for exclude().

    # Roughly: SELECT blog_blog.*
    # FROM blog_blog
    # WHERE NOT (EXISTS
    #              (SELECT 1 AS a
    #               FROM blog_entry U1
    #               WHERE (U1.headline LIKE %Lennon%
    #                      AND U1.blog_id = (blog_blog.id))
    #               LIMIT 1)
    #            AND EXISTS
    #              (SELECT 1 AS a
    #               FROM blog_entry U1
    #               WHERE (U1.pub_date BETWEEN 2008-01-01 AND 2008-12-31
    #                      AND U1.blog_id = (blog_blog.id))
    #               LIMIT 1))
    Blog.objects.exclude(entry__headline__contains='Lennon',
                         entry__pub_date__year=2008)

    # Roughly: SELECT blog_blog.*
    # FROM blog_blog
    # WHERE NOT (EXISTS
    #              (SELECT 1 AS a
    #               FROM blog_entry V1
    #               WHERE (V1.id IN
    #                        (SELECT U0.id
    #                         FROM blog_entry U0
    #                         WHERE (U0.headline LIKE %Lennon%
    #                                AND U0.pub_date BETWEEN 2008-01-01 AND 2008-12-31))
    #                      AND V1.blog_id = (blog_blog.id))
    #               LIMIT 1))
    Blog.objects.exclude(entry__in=Entry.objects.filter(
        headline__contains='Lennon', pub_date__year=2008
    ))


def field_lookup_f_expressions():
    # Roughly: SELECT * FROM blog_entry WHERE number_of_comments > number_of_pingbacks;
    Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks'))

    # Roughly: SELECT * FROM blog_entry WHERE number_of_comments > (number_of_pingbacks * 2);
    Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks') * 2)

    # Roughly: SELECT * FROM blog_entry WHERE rating < (number_of_comments + number_of_pingbacks);
    Entry.objects.filter(rating__lt=F('number_of_comments') + F('number_of_pingbacks'))

    # Roughly: SELECT blog_entry.* FROM blog_entry
    # INNER JOIN blog_blog ON (blog_entry.blog_id = blog_blog.id)
    # INNER JOIN blog_entry_authors ON (blog_entry.id = blog_entry_authors.entry_id)
    # INNER JOIN blog_author ON (blog_entry_authors.author_id = blog_author.id)
    # WHERE blog_author.name = (blog_blog.name)
    Entry.objects.filter(authors__name=F('blog__name'))

    # Roughly: SELECT * FROM blog_entry WHERE mod_date > (django_format_dtdelta(\'+\', pub_date, 259200000000))
    # Return all entries that were modified more than 3 days after they were published
    Entry.objects.filter(mod_date__gt=F('pub_date') + datetime.timedelta(days=3))

    # Roughly: SELECT * FROM blog_entry WHERE number_of_comments > (number_of_pingbacks & 16);
    Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks').bitand(16))


def field_lookup_transforms():
    # Roughly: SELECT * FROM blog_entry
    # WHERE django_date_extract(year, pub_date) = (django_date_extract(year, mod_date))
    Entry.objects.filter(pub_date__year=F('mod_date__year'))

    # Find the earliest year an entry was published
    Entry.objects.aggregate(first_published_year=Min('pub_date__year'))

    # Finds the value of the highest rated entry and the total number of comments on all entries for each year
    Entry.objects.values('pub_date__year').annotate(
        top_rating=Subquery(
            Entry.objects.filter(
                pub_date__year=OuterRef('pub_date__year')
            ).order_by('-rating').values('rating')[:1]
        ),
        total_comments=Sum('number_of_comments'))


def field_lookup_primary_key():
    # Roughly: SELECT * FROM blog_blog WHERE id = 14
    Blog.objects.get(id__exact=14)  # Explicit form
    Blog.objects.get(id=14)  # __exact is implied
    Blog.objects.get(pk=14)  # pk implies id__exact

    # Roughly: SELECT * FROM blog_blog WHERE IN (1, 4, 7)
    Blog.objects.filter(pk__in=[1, 4, 7])

    # Roughly: SELECT * FROM blog_blog WHERE id > 14
    Blog.objects.filter(pk__gt=14)

    # pk lookups also work across joins
    # Roughly: SELECT * FROM blog_entry WHERE blog_entry.blog_id = 3
    Entry.objects.filter(blog__id__exact=3)  # Explicit form
    Entry.objects.filter(blog__id=3)  # __exact is implied
    Entry.objects.filter(blog__pk=3)  # __pk implies __id__exact


def field_lookup_json():
    # Roughly: INSERT INTO blog_dog (name, data) VALUES ('Max', NULL)
    Dog.objects.create(name='Max', data=None)  # SQL NULL.

    # Roughly: INSERT INTO blog_dog (name, data) VALUES ('Archie', 'null')
    Dog.objects.create(name='Archie', data=Value('null'))  # JSON null.


def field_lookup_json_transforms():
    # Roughly: INSERT INTO blog_dog (name, data)
    # VALUES ('Rufus', '{"breed": "labrador", "owner": {"name": "Bob", other_pets": [{"name": "Fishy"}]}}'
    Dog.objects.create(name='Rufus', data={
        'breed': 'labrador',
        'owner': {
            'name': 'Bob',
            'other_pets': [{
                'name': 'Fishy',
            }],
        },
    })
    # Roughly: INSERT INTO blog_dog (name, data)
    # VALUES ('Meg', '{"breed": "collie", "owner": null}')
    Dog.objects.create(name='Meg', data={'breed': 'collie', 'owner': None})

    # Roughly: SELECT * FROM blog_dog
    # WHERE (
    # 		CASE
    # 			WHEN JSON_TYPE('data, '$."breed"') IN ('true', 'null', 'false')
    # 				THEN JSON_TYPE('data, '$."breed"')
    # 			ELSE JSON_EXTRACT('data, '$."breed"')
    # 			END
    # 		) = JSON_EXTRACT('"collie"', '$')
    Dog.objects.filter(data__breed='collie')

    # Roughly: SELECT * FROM blog_dog
    # WHERE (
    #       CASE
    #           WHEN JSON_TYPE(data, '$."owner"."name"') IN ('true','null','false')
    #               THEN JSON_TYPE(data, '$."owner"."name"')
    #           ELSE JSON_EXTRACT(data, '$."owner"."name"')
    #           END
    #       ) = JSON_EXTRACT('"Bob"', '$')'
    Dog.objects.filter(data__owner__name='Bob')

    # Roughly: SELECT * FROM blog_dog
    # WHERE (
    # 		CASE
    # 			WHEN JSON_TYPE(data, '$."owner"."other_pets"[0]."name"') IN ('false' ,'null' ,'true')
    # 				THEN JSON_TYPE(data, '$."owner"."other_pets"[0]."name"')
    # 			ELSE JSON_EXTRACT(data, '$."owner"."other_pets"[0]."name"')
    # 			END
    # 		) = JSON_EXTRACT('"Fishy"', '$')
    Dog.objects.filter(data__owner__other_pets__0__name='Fishy')

    # Roughly: SELECT * FROM blog_dog WHERE JSON_TYPE(data, '$."owner"') IS NULL
    Dog.objects.filter(data__owner__isnull=True)

    Dog.objects.filter(data__contains={'owner': 'Bob'})

    Dog.objects.filter(data__contained_by={'breed': 'collie'})

    # Roughly: SELECT * FROM blog_dog WHERE JSON_TYPE(data, '$."owner"') IS NOT NULL
    Dog.objects.filter(data__has_key='owner')

    # Roughly: SELECT * FROM blog_dog
    # WHERE (
    # 		JSON_TYPE(data, '$."breed"') IS NOT NULL
    # 		AND JSON_TYPE(data, '$."owner"') IS NOT NULL
    # 		)
    Dog.objects.filter(data__has_keys=['breed', 'owner'])

    # Roughly: SELECT * FROM blog_dog
    # WHERE (
    # 		JSON_TYPE(data, '$."owner"') IS NOT NULL
    # 		OR JSON_TYPE(data, '$."breed"') IS NOT NULL
    # 		)
    Dog.objects.filter(data__has_any_keys=['owner', 'breed'])


def comparing_objects():
    entry_1 = Entry.objects.get(pk=1)
    entry_2 = Entry.objects.get(pk=2)
    result = entry_1 == entry_2  # Equivalent to entry_1.id == entry_2.id


def deleting_objects():
    entry_1 = Entry.objects.get(pk=1)
    entry_1.delete()

    # Executed purely in SQL, so delete() methods of individual object
    # instances will not necessarily be called during the process.
    Entry.objects.filter(pub_date__year=2005).delete()


def copying_model_instances():
    blog = Blog(name='My blog', tagline='Blogging is easy')
    blog.save()  # blog.pk == 1

    blog.pk = None
    blog._state.adding = True
    blog.save()  # blog.pk == 2


def copying_model_inheritance_instances():
    # Roughly:
    # BEGIN
    # INSERT INTO blog_blog (name, taglin")
    # VALUES ('Django', 'Django is easy')
    # INSERT INTO blog_themeblog (blog_ptr_id, theme) VALUES (2, 'python'),
    blog = ThemeBlog(name='Django', tagline='Django is easy', theme='python')
    blog.save()  # django_blog.pk == 2

    blog.pk = None
    blog.id = None
    blog._state.adding = True
    blog.save()  # django_blog.pk == 3
    # Roughly:
    # BEGIN
    # INSERT INTO blog_blog (name, tagline) VALUES ('Django', 'Django is easy')
    # INSERT INTO blog_themeblog (blog_ptr_id, theme) VALUES (3, 'python')


def copying_model_instances_with_many_to_many_field():
    entry = Entry.objects.all()[0]  # entry.pk == 1
    old_authors = entry.authors.all()  # <QuerySet [<Author: Joe>, <Author: John>, <Author: Paul>]>
    entry.pk = None
    entry._state.adding = True
    
    # Roughly:
    # INSERT INTO blog_entry (blog_id, headline, body_text, pub_date, mod_date, number_of_comments, number_of_pingbacks, rating)
    # VALUES (1, '', '', '2000-12-31', '2022-08-25', 0, 0, 5)
    entry.save()

    # Roughly:
    # SELECT "blog_author"."id", "blog_author"."name", "blog_author"."email" FROM "blog_author" INNER JOIN "blog_entry_authors" ON ("blog_author"."id" = "blog_entry_authors"."author_id") WHERE "blog_entry_authors"."entry_id" = 1
    # BEGIN
    # SELECT "blog_author"."id" FROM "blog_author" INNER JOIN "blog_entry_authors" ON ("blog_author"."id" = "blog_entry_authors"."author_id") WHERE "blog_entry_authors"."entry_id" = 1
    entry.authors.set(old_authors)


def copying_model_instances_with_many_to_many_field():
    entry = Entry.objects.get(pk=5)
    detail = EntryDetail.objects.get(pk=1)

    detail.pk = None
    detail._state.adding = True
    detail.entry = entry
    # Roughly: INSERT INTO blog_entrydetail (entry_id, details) VALUES (5, 'Extra details')
    detail.save()


def update_multiple_objects():
    # Roughly: UPDATE blog_entry SET headline = 'Everything is the same'
    # WHERE blog_entry.pub_date BETWEEN '2007-01-01' AND '2007-12-31'
    Entry.objects.filter(pub_date__year=2007).update(headline='Everything is the same')

    # Roughly: UPDATE blog_entry SET number_of_pingbacks = (blog_entry.number_of_pingbacks + 1)
    Entry.objects.all().update(number_of_pingbacks=F('number_of_pingbacks') + 1)


def update_multiple_objects_foreign_key_field():
    blog = Blog.objects.get(pk=1)
    # Roughly: UPDATE blog_entry SET blog_id = 1
    # WHERE blog_entry.pub_date BETWEEN '2007-01-01' AND '2007-12-31'
    Entry.objects.filter(pub_date__year=2007).update(headline='Everything is the same')


def foreign_key_select_related():
    e = Entry.objects.get(id=2)
    print(e.blog)  # Hits the database to retrieve the associated Blog.
    print(e.blog)  # Doesn't hit the database; uses cached version.

    # Roughly:
    # SELECT blog_entry.* , blog_blog.* FROM blog_entry
    # INNER JOIN blog_blog ON (blog_entry.blog_id = blog_blog.id) WHERE blog_entry.id = 1
    e = Entry.objects.select_related().get(id=2)
    print(e.blog)  # Doesn't hit the database; uses cached version.
    print(e.blog)  # Doesn't hit the database; uses cached version.


def backward_relationship():
    b = Blog.objects.get(id=1)
    b.entry_set.all()  # Returns all Entry objects related to Blog.

    # b.entry_set is a Manager that returns QuerySets.
    b.entry_set.filter(headline__contains='Lennon')
    b.entry_set.count()


def field_lookup_over_related_objects():
    b = Blog.objects.get(pk=1)

    Entry.objects.filter(blog=b)


def custom_lookup():
    # Roughly: SELECT * FROM blog_author WHERE name <> 'Jack'
    Author.objects.filter(name__ne='Jack')


def transformer_lookup():
    # Roughly: SELECT * FROM blog_entry WHERE ABS(rating) = 5.0
    Entry.objects.filter(rating__abs=5)

    # Roughly: SELECT * FROM blog_entry WHERE rating < 5.0 AND rating > -5.0
    Entry.objects.filter(rating__abs__lt=5)


def bilateral_transformer_lookup():
    # Roughly: SELECT * FROM blog_author WHERE UPPER(name) = UPPER('doe')
    Author.objects.filter(name__upper="doe")
