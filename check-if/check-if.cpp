#include "clang/Frontend/FrontendActions.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"
// Declares llvm::cl::extrahelp.
#include "llvm/Support/CommandLine.h"
#include "clang/ASTMatchers/ASTMatchers.h"
#include "clang/ASTMatchers/ASTMatchFinder.h"
#include  "clang/AST/Type.h"
#include<iostream>

using namespace std;
using namespace clang::tooling;
using namespace llvm;
using namespace clang;
using namespace clang::ast_matchers;

// Apply a custom category to all command-line options so that they are the
// only ones displayed.
static llvm::cl::OptionCategory MyToolCategory("my-tool options");

// CommonOptionsParser declares HelpMessage with a description of the common
// command-line options related to the compilation database and input files.
// It's nice to have this help message in all tools.
static cl::extrahelp CommonHelp(CommonOptionsParser::HelpMessage);

// A help message for this specific tool can be added afterwards.
static cl::extrahelp MoreHelp("\nMore help text...");

StatementMatcher LoopMatcher=
 ifStmt(hasCondition(ignoringParenImpCasts(binaryOperator(hasOperatorName("=")).bind("ifLoop"))));


StatementMatcher LoopMatcher1=
 whileStmt(hasCondition(ignoringParenImpCasts(binaryOperator(hasOperatorName("=")).bind("whileLoop"))));

int n=0;
class LoopPrinter : public MatchFinder::MatchCallback {
public :
  virtual void run(const MatchFinder::MatchResult &Result) {
	
	
	if (const BinaryOperator *FS = Result.Nodes.getNodeAs<clang::BinaryOperator>("ifLoop"))
	{	FullSourceLoc fullLoc(FS->getLocStart(),Result.Context->getSourceManager());
		
		const std::string &fileName = Result.SourceManager->getFilename(fullLoc);
		const unsigned int lineNum = fullLoc.getSpellingLineNumber();	
		const unsigned int columnNum = fullLoc.getSpellingColumnNumber();
        cout<<fileName<<" "<<lineNum<<" "<<columnNum<<" err_if";
	}
  
	if (const BinaryOperator *FS = Result.Nodes.getNodeAs<clang::BinaryOperator>("whileLoop"))
	{	FullSourceLoc fullLoc(FS->getLocStart(),Result.Context->getSourceManager());
		
		const std::string &fileName = Result.SourceManager->getFilename(fullLoc);
		const unsigned int lineNum = fullLoc.getSpellingLineNumber(); 
		const unsigned int columnNum = fullLoc.getSpellingColumnNumber();
		cout<<fileName<<" "<<lineNum<<" "<<columnNum<<" err_if";
	}
}
};


int main(int argc, const char **argv) {
  CommonOptionsParser OptionsParser(argc, argv, MyToolCategory);
  ClangTool Tool(OptionsParser.getCompilations(),
                 OptionsParser.getSourcePathList());

  LoopPrinter Printer;
  MatchFinder Finder;
  Finder.addMatcher(LoopMatcher, &Printer);
  Finder.addMatcher(LoopMatcher1, &Printer);
  return Tool.run(newFrontendActionFactory(&Finder).get());
}
