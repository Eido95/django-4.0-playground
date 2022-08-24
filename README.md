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
* [Using Django (topics)](https://docs.djangoproject.com/en/4.0/topics/)
  * ✅ [Models](https://docs.djangoproject.com/en/4.0/topics/db/models/)
  * ✅ [Migrations](https://docs.djangoproject.com/en/4.0/topics/migrations/)
    * 🧰 [Serializing values](https://docs.djangoproject.com/en/4.0/topics/migrations/#serializing-values)
* [Django FAQ](https://docs.djangoproject.com/en/4.0/faq/)
* [General Index](https://docs.djangoproject.com/en/4.0/genindex/)
* [API Reference](https://docs.djangoproject.com/en/4.0/ref/)
  * 🧰 [Field options](https://docs.djangoproject.com/en/4.0/ref/models/fields/#field-options)
  * 🧰 [Field types](https://docs.djangoproject.com/en/4.0/ref/models/fields/#model-field-types)

## Insights

* Prefer intermediate model (using `through` argument) over 
  plain `ManyToManyField` (due to migration [overhead](https://docs.djangoproject.com/en/4.0/howto/writing-migrations/#changing-a-manytomanyfield-to-use-a-through-model))

## Issues

* When executing `startapp`, ask for permission to continue if `manage.py` 
  file not exists in working directory.