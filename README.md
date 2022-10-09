# Django 4.0 Playground

https://docs.djangoproject.com/en/4.0/

## What to read next

* ✅ [Meta-documentation and miscellany](https://docs.djangoproject.com/en/4.0/misc/)
  * ✅ [API stability](https://docs.djangoproject.com/en/4.0/misc/api-stability/)
  * ✅ [Design philosophies](https://docs.djangoproject.com/en/4.0/misc/design-philosophies/)
  * ✅ [Third-party distributions of Django](https://docs.djangoproject.com/en/4.0/misc/distributions/)
* [“How-to” guides](https://docs.djangoproject.com/en/4.0/howto/)
  * ❌ [How to authenticate using `REMOTE_USER`](https://docs.djangoproject.com/en/4.0/howto/auth-remote-user/)
  * ✅ [How to create custom `django-admin` commands](https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/)
  * ✅ [How to create database migrations](https://docs.djangoproject.com/en/4.0/howto/writing-migrations/)
  * ✅ [How to create custom model fields](https://docs.djangoproject.com/en/4.0/howto/custom-model-fields/)
  * ✅ [How to write custom lookups](https://docs.djangoproject.com/en/4.0/howto/custom-lookups/)
    * 🧰 [How Django determines the lookups and transforms which are used](https://docs.djangoproject.com/en/4.0/howto/custom-lookups/#how-django-determines-the-lookups-and-transforms-which-are-used)
  * ❌ [How to implement a custom template backend](https://docs.djangoproject.com/en/4.0/howto/custom-template-backend/)
* [Using Django (topics)](https://docs.djangoproject.com/en/4.0/topics/)
  * ✅ [Models](https://docs.djangoproject.com/en/4.0/topics/db/models/)
  * ✅ [Making queries](https://docs.djangoproject.com/en/4.0/topics/db/queries/)
    * 🧰 [Caching and QuerySets](https://docs.djangoproject.com/en/4.0/topics/db/queries/#caching-and-querysets)
    * 🧰 [Additional methods to handle related objects](https://docs.djangoproject.com/en/4.0/topics/db/queries/#additional-methods-to-handle-related-objects)
  * ✅ [Class-based views](https://docs.djangoproject.com/en/4.0/topics/class-based-views/#class-based-views)
    * ✅ [Introduction to class-based views](Introduction to class-based views)
  * ✅ [Migrations](https://docs.djangoproject.com/en/4.0/topics/migrations/)
    * 🧰 [Serializing values](https://docs.djangoproject.com/en/4.0/topics/migrations/#serializing-values)
  * 🛡 [Cross site request forgery (CSRF) protection](https://docs.djangoproject.com/en/4.0/topics/security/#cross-site-request-forgery-csrf-protection)
  * ✅ [How to use sessions](https://docs.djangoproject.com/en/4.0/topics/http/sessions/)
* [Django FAQ](https://docs.djangoproject.com/en/4.0/faq/)
  * 🧰 [How can I see the raw SQL queries Django is running?](https://docs.djangoproject.com/en/4.0/faq/models/#how-can-i-see-the-raw-sql-queries-django-is-running)
* [General Index](https://docs.djangoproject.com/en/4.0/genindex/)
* [API Reference](https://docs.djangoproject.com/en/4.0/ref/)
  * 🧰 [Field options](https://docs.djangoproject.com/en/4.0/ref/models/fields/#field-options)
  * 🧰 [Field types](https://docs.djangoproject.com/en/4.0/ref/models/fields/#model-field-types)
  * 🧰 [Field lookups](https://docs.djangoproject.com/en/4.0/ref/models/querysets/#field-lookups)
  * 🧰 [When QuerySets are evaluated](https://docs.djangoproject.com/en/4.0/ref/models/querysets/#when-querysets-are-evaluated)
  * 🛡️ [Cross Site Request Forgery protection](https://docs.djangoproject.com/en/4.0/ref/csrf/)
  * 🧰 [Sessions Settings](https://docs.djangoproject.com/en/4.0/ref/settings/#sessions)

## Insights

* Prefer intermediate model (using `through` argument) over 
  plain `ManyToManyField` (due to migration [overhead](https://docs.djangoproject.com/en/4.0/howto/writing-migrations/#changing-a-manytomanyfield-to-use-a-through-model))
* Prefer `None` over `Value(null)` as the top-level value 
  of `JSONField(null=True)` following [recommendation](https://docs.djangoproject.com/en/4.0/topics/db/queries/#storing-and-querying-for-none)

## Issues

* When executing `startapp`, ask for permission to continue if `manage.py` 
  file not exists in working directory.

## Questions
* What is "parenthetical grouping" in [Complex lookups with Q objects](https://docs.djangoproject.com/en/4.0/topics/db/queries/#complex-lookups-with-q-objects)?
