echo 'Running lexerTest'
python tests/lexerTest.py ;
echo 'Running parserTest'
python tests/parserTest.py ;
echo 'Running semanticTest'
python tests/semanticTest.py ;
echo 'Running pythonGeneratorTest'
python tests/pythonGeneratorTest.py ;

python tests/mainTest.py other/expressionsTest.cpp;
python tests/mainTest.py other/nestedReferencesTest.cpp;
python tests/mainTest.py other/classesTest.cpp;
python tests/mainTest.py other/generalTest.cpp;
python tests/mainTest.py other/passTest.cpp;
python tests/mainTest.py other/c.cpp;
python tests/mainTest.py other/c2.cpp;