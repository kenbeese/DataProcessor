DataProcessor
=============

A data processing library.

Sample usage is written in `sample/README.md`


Build documentation
===================
Requirements

- sphinx (python documentation tools)
- numpydoc (Sphinx extention)

If you have not installed these,

    easy_install sphinx numpydoc

After installation of above library,
you can make api reference of this library with following command.

    make -C doc html

`doc/_build/html/index.html` is top page.

If you add new file to `lib/dataprocessor` or delete file from `lib/dataprocessor`,
please use following command before above command.

    make -C doc updateref
    make -C doc html


Lisence
==========
GPLv3
