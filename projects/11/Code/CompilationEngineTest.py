#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      bla
#
# Created:     14/12/2015
# Copyright:   (c) bla 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import unittest
import CompilationEngine
import StringIO

class CompilationEngineTest(unittest.TestCase):

    def test_CompileEmptyClass(self):
        ipt=StringIO.StringIO("""class id\n
        {\n}\n""")
        opt=StringIO.StringIO("")
        target_string="""<class>
<keyword> class </keyword>
<identifier> id </identifier>
<symbol> { </symbol>
<symbol> } </symbol>
</class>
"""
        comp=CompilationEngine.CompilationEngine(ipt,opt,True)
        comp.CompileClass()
        opt.seek(0)
        res=opt.read()
        self.assertEquals(res,target_string)

    def test_CompileClassVarDec(self):
        # add extraneaous ; because token must be advanced
        ipt=StringIO.StringIO("""static int name,name;;""")
        opt=StringIO.StringIO("")
        target_string="""<classVarDec>
<keyword> static </keyword>
<keyword> int </keyword>
<identifier> name </identifier>
<symbol> , </symbol>
<identifier> name </identifier>
<symbol> ; </symbol>
</classVarDec>
"""
        comp=CompilationEngine.CompilationEngine(ipt,opt,True)
        comp.CompileClassVarDec()
        opt.seek(0)
        res=opt.read()
        self.assertEquals(res,target_string)

    def test_CompileParameterList(self):
        # add extraneaous ; because token must be advanced
        ipt=StringIO.StringIO("""int name,int name;""")
        opt=StringIO.StringIO("")
        target_string="""<parameterList>
<keyword> int </keyword>
<identifier> name </identifier>
<symbol> , </symbol>
<keyword> int </keyword>
<identifier> name </identifier>
</parameterList>
"""
        comp=CompilationEngine.CompilationEngine(ipt,opt,True)
        comp.CompileParameterList()
        opt.seek(0)
        res=opt.read()
        self.assertEquals(res,target_string)

    def test_CompileReturn(self):
        # add extraneaous ; because token must be advanced
        ipt=StringIO.StringIO("""return;;""")
        opt=StringIO.StringIO("")
        target_string="""<returnStatement>
<keyword> return </keyword>
<symbol> ; </symbol>
</returnStatement>
"""
        comp=CompilationEngine.CompilationEngine(ipt,opt,True)
        comp.CompileReturn()
        opt.seek(0)
        res=opt.read()
        self.assertEquals(res,target_string)

    def test_CompileVarDec(self):
        ipt=StringIO.StringIO("""var int name,name;;""")
        opt=StringIO.StringIO("")
        target_string="""<varDec>
<keyword> var </keyword>
<keyword> int </keyword>
<identifier> name </identifier>
<symbol> , </symbol>
<identifier> name </identifier>
<symbol> ; </symbol>
</varDec>
"""
        comp=CompilationEngine.CompilationEngine(ipt,opt,True)
        comp.CompileVarDec()
        opt.seek(0)
        res=opt.read()
        self.assertEquals(res,target_string)

    def test_CompileStatements(self):
        ipt=StringIO.StringIO("""return;return;;""")
        opt=StringIO.StringIO("")
        target_string="""<statements>
<returnStatement>
<keyword> return </keyword>
<symbol> ; </symbol>
</returnStatement>
<returnStatement>
<keyword> return </keyword>
<symbol> ; </symbol>
</returnStatement>
</statements>
"""
        comp=CompilationEngine.CompilationEngine(ipt,opt,True)
        comp.CompileStatements()
        opt.seek(0)
        res=opt.read()
        self.assertEquals(res,target_string)

    def test_CompileDo(self):
        ipt=StringIO.StringIO("""do blah.blih();;""")
        opt=StringIO.StringIO("")
        target_string="""<doStatement>
<keyword> do </keyword>
<identifier> blah </identifier>
<symbol> . </symbol>
<identifier> blih </identifier>
<symbol> ( </symbol>
<expressionList>
</expressionList>
<symbol> ) </symbol>
<symbol> ; </symbol>
</doStatement>
"""
        comp=CompilationEngine.CompilationEngine(ipt,opt,True)
        comp.CompileDo()
        opt.seek(0)
        res=opt.read()
        self.assertEquals(res,target_string)

    def test_CompileLet(self):
        ipt=StringIO.StringIO("""let blob[foo]=foo;;""")
        opt=StringIO.StringIO("")
        target_string="""<letStatement>
<keyword> let </keyword>
<identifier> blob </identifier>
<symbol> [ </symbol>
<expression>
<term>
<identifier> foo </identifier>
</term>
</expression>
<symbol> ] </symbol>
<symbol> = </symbol>
<expression>
<term>
<identifier> foo </identifier>
</term>
</expression>
<symbol> ; </symbol>
</letStatement>
"""
        comp=CompilationEngine.CompilationEngine(ipt,opt,True)
        comp.CompileLet()
        opt.seek(0)
        res=opt.read()
        self.assertEquals(res,target_string)

    def test_CompileWhile(self):
        ipt=StringIO.StringIO("""while(foo){return bar;};""")
        opt=StringIO.StringIO("")
        target_string="""<whileStatement>
<keyword> while </keyword>
<symbol> ( </symbol>
<expression>
<term>
<identifier> foo </identifier>
</term>
</expression>
<symbol> ) </symbol>
<symbol> { </symbol>
<statements>
<returnStatement>
<keyword> return </keyword>
<expression>
<term>
<identifier> bar </identifier>
</term>
</expression>
<symbol> ; </symbol>
</returnStatement>
</statements>
<symbol> } </symbol>
</whileStatement>
"""
        comp=CompilationEngine.CompilationEngine(ipt,opt,True)
        comp.CompileWhile()
        opt.seek(0)
        res=opt.read()
        self.assertEquals(res,target_string)

    def test_CompileIf(self):
        ipt=StringIO.StringIO("""if(foo){return foo;}else{return foo;};""")
        opt=StringIO.StringIO("")
        target_string="""<ifStatement>
<keyword> if </keyword>
<symbol> ( </symbol>
<expression>
<term>
<identifier> foo </identifier>
</term>
</expression>
<symbol> ) </symbol>
<symbol> { </symbol>
<statements>
<returnStatement>
<keyword> return </keyword>
<expression>
<term>
<identifier> foo </identifier>
</term>
</expression>
<symbol> ; </symbol>
</returnStatement>
</statements>
<symbol> } </symbol>
<keyword> else </keyword>
<symbol> { </symbol>
<statements>
<returnStatement>
<keyword> return </keyword>
<expression>
<term>
<identifier> foo </identifier>
</term>
</expression>
<symbol> ; </symbol>
</returnStatement>
</statements>
<symbol> } </symbol>
</ifStatement>
"""
        comp=CompilationEngine.CompilationEngine(ipt,opt,True)
        comp.CompileIf()
        opt.seek(0)
        res=opt.read()
        self.assertEquals(res,target_string)

    def test_CompileSubroutine(self):
        ipt=StringIO.StringIO("""function void test(int blob,foo bar){var int test; return (3+"foo");};""")
        opt=StringIO.StringIO("")
        target_string="""<subroutineDec>
<keyword> function </keyword>
<keyword> void </keyword>
<identifier> test </identifier>
<symbol> ( </symbol>
<parameterList>
<keyword> int </keyword>
<identifier> blob </identifier>
<symbol> , </symbol>
<identifier> foo </identifier>
<identifier> bar </identifier>
</parameterList>
<symbol> ) </symbol>
<subroutineBody>
<symbol> { </symbol>
<varDec>
<keyword> var </keyword>
<keyword> int </keyword>
<identifier> test </identifier>
<symbol> ; </symbol>
</varDec>
<statements>
<returnStatement>
<keyword> return </keyword>
<expression>
<term>
<symbol> ( </symbol>
<expression>
<term>
<integerConstant> 3 </integerConstant>
</term>
<symbol> + </symbol>
<term>
<stringConstant> foo </stringConstant>
</term>
</expression>
<symbol> ) </symbol>
</term>
</expression>
<symbol> ; </symbol>
</returnStatement>
</statements>
<symbol> } </symbol>
</subroutineBody>
</subroutineDec>
"""
        comp=CompilationEngine.CompilationEngine(ipt,opt,True)
        comp.CompileSubroutine()
        opt.seek(0)
        res=opt.read()
        self.assertEquals(res,target_string)


if __name__ == '__main__':
    unittest.main()
