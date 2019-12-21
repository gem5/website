---
layout: documentation
title: ISA Parser
doc: gem5 documentation
parent: architecture_support
permalink: documentation/general_docs/architecture_support/isa_parser/
---

# ISA Parser

The gem5 ISA description language is a custom language designed specifically for generating the class definitions and decoder function needed by gem5. This section provides a practical, informal overview of the language itself. A formal grammar for the language is embedded in the "yacc" portion of the parser (look for the functions starting with p\_ in isa\_parser.py). A second major component of the parser processes C-like code specifications to extract instruction characteristics; this aspect is covered in the section [Code parsing](#code-parsing).
At the highest level, an ISA description file is divided into two parts: a declarations section and a decode section. The decode section specifies the structure of the decoder and defines the specific instructions returned by the decoder. The declarations section defines the global information (classes, instruction formats, templates, etc.) required to support the decoder. Because the decode section is the focus of the description file, we will begin the discussion there.

## The decode section

The decode section of the description is a set of nested decode blocks. A decode block specifies a field of a machine instruction to decode and the result to be provided for particular values of that field. A decode block is similar to a C switch statement in both syntax and semantics. In fact, each decode block in the description file generates a switch statement in the resulting decode function.
Let's begin with a (slightly oversimplified) example:

{% raw %}
```
decode OPCODE {
  0: add({{ Rc = Ra + Rb; }});
  1: sub({{ Rc = Ra - Rb; }});
}
```
{% endraw %}

A decode block begins with the keyword `decode` followed by the name of the instruction field to decode. The latter must be defined in the declarations section of the file using a bitfield definition (see [Bitfield definitions](#bitfield-definitions)). The remainder of the decode block is a list of statements enclosed in braces. The most common statement is an integer constant and a colon followed by an instruction definition. This statement corresponds to a 'case' statement in a C switch (but note that the 'case' keyword is omitted for brevity). A comma-separated list of integer constants may be used to allow a single decode statement to apply to any of a set of bitfield values.

{% raw %}
Instruction definitions are similar in syntax to C function calls, with the instruction mnemonic taking the place of the function name. The comma-separated arguments are used when processing the instruction definition. In the example above, the instruction definitions each take a single argument, a ''code literal''. A code literal is operationally similar to a string constant, but is delimited by double braces (`{{` and `}}`). Code literals may span multiple lines without escaping the end-of-line characters. No backslash escape processing is performed (e.g., `\t` is taken literally, and does not produce a tab). The delimiters were chosen so that C-like code contained in a code literal would be formatted nicely by emacs C-mode.
{% endraw %}

A decode statement may specify a nested decode block in place of an instruction definition. In this case, if the bitfield specified by the outer block matches the given value(s), the bitfield specified by the inner block is examined and an additional switch is performed.

It is also legal, as in C, to use the keyword `default` in place of an integer constant to define a default action. However, it is more common to use the decode-block default syntax discussed in the section [Decode block defaults](#decode-block-defaults) below.

### Specifying instruction formats

When the ISA description file is processed, each instruction definition does in fact invoke a function call to generate the appropriate C++ code for the decode file. The function that is invoked is determined by the instruction format. The instruction format determines the number and type of the arguments given to the instruction definition, and how they are processed to generate the corresponding output. Note that the term "instruction format" as used in this context refers solely to one of these definition-processing functions, and does not necessarily map one-to-one to the machine instruction formats defined by the ISA.
The one oversimplification in the previous example is that no instruction format was specified. As a result, the parser does not know how to process the instruction definitions.

Instruction formats can be specified in two ways. An explicit format specification can be given before the mnemonic, separated by a double colon (::), as follows:


{% raw %}
```
decode OPCODE {
  0: Integer::add({{ Rc = Ra + Rb; }});
  1: Integer::sub({{ Rc = Ra - Rb; }});
}
```
{% endraw %}

In this example, both instruction definitions will be processed using the format Integer. A more common approach specifies the format for a set of definitions using a format block, as follows:

{% raw %}
```
decode OPCODE {
  format Integer {
    0: add({{ Rc = Ra + Rb; }});
    1: sub({{ Rc = Ra - Rb; }});
  }
}
```
{% endraw %}

In this example, the format "Integer" applies to all of the instruction definitions within the inner braces. The two examples are thus functionally equivalent. There are few restrictions on the use of format blocks. A format block may include only a subset of the statements in a decode block. Format blocks and explicit format specifications may be mixed freely, with the latter taking precedence. Format and decode blocks can be nested within each other arbitrarily. Note that a closing brace will always bind with the nearest format or decode block, making it syntactically impossible to generate format or decode blocks that do not nest fully inside the enclosing block.

At any point where an instruction definition occurs without an explicit format specification, the format associated with the innermost enclosing format block will be used. If a definition occurs with no explicit format and no enclosing format block, a runtime error will be raised.

### Decode block defaults

Default cases for decode blocks can be specified by `default:` labels, as in C switch statements. However, it is common in ISA descriptions that unspecified cases correspond to unknown or illegal instruction encodings. To avoid the requirement of a `default:` case in every decode block, the language allows an alternate default syntax that specifies a default case for the current decode block and any nested decode block with no explicit default. This alternate default is specified by giving the `default` keyword and an instruction definition after the bitfield specification (prior to the opening brace). Specifying the outermost decode block as follows:

```
decode OPCODE default Unknown::unknown() {
   [...]
}
```

is thus (nearly) equivalent to adding `default: Unknown::unknown();` inside every decode block that does not otherwise specify a default case.

_Note: The appropriate format definition (see _[Format definitions](#format-definitions)_) is invoked each time an instruction definition is encountered.  Thus there is a semantic difference between having a single block-level default and a default within each nested block, which is that the former will invoke the format definition once, while the latter could result in multiple invocations of the format definition.  If the format definition generates header, decoder, or exec output, then that output will be included multiple times in the corresponding files, which typically leads to multiple definition errors when the C++ gets compiled.  If it is absolutely necessary to invoke the format definition for a single instruction multiple times, the format definition should be written to produce _only_ decode-block output, and all needed header, decoder, and exec output should be produced once using_ `output` _blocks (see _[Output blocks](#output-blocks])_)._

### Preprocessor directive handling

The decode block may also contain C preprocessor directives. These directives are not processed by the parser; instead, they are passed through to the C++ output to be processed when the C++ decoder is compiled. The parser does not recognize any specific directives; any line with a # in the first column is treated as a preprocessor directive.
The directives are copied to all of the output streams (the header, the decoder, and the execute files; see [Format definitions](#format-definitions). The directives maintain their position relative to the code generated by the instruction definitions within the decode block. The net result is that, for example, #ifdef/#endif pairs that surround a set of instruction definitions will enclose both the declarations generated by those definitions and the corresponding case statements within the decode function. Thus #ifdef and similar constructs can be used to delineate instruction definitions that will be conditionally compiled into the simulator based on preprocessor symbols (e.g., FULL\_SYSTEM). It should be emphasized that #ifdef does not affect the ISA description parser. In an #ifdef/#else/#endif construct, all of the instruction definitions in both parts of the conditional will be processed. Only during the subsequent C++ compilation of the decoder will one or the other set of definitions be selected.

## The declaration section

As mentioned above, the decode section of the ISA description (consisting of a single outer decode block) is preceded by the declarations section. The primary purpose of the declarations section is to define the instruction formats and other supporting elements that will be used in the decode block, as well as supporting C++ code that is passed almost verbatim to the generated output.
This section describes the components that appear in the declaration section: [Format definitions](#format-definitions), [Template definitions](#template-definitions), [Output blocks](#output-blocks), [Let blocks](#let-blocks), [Bitfield definitions](#bitfield-definitions), [Operand and operand type definitions](#operand-and-operand-type-definitions), and [Namespace declaration](#namespace-declaration).

### Format definitions

An instruction format is basically a Python function that takes the arguments supplied by an instruction definition (found inside a decode block) and generates up to four pieces of C++ code. The pieces of C++ code are distinguished by where they appear in the generated output.
 1. The ''header output'' goes in the header file (decoder.hh) that is included in all the generated source files (decoder.cc and all the per-CPU-model execute .cc files). The header output typically contains the C++ class declaration(s) (if any) that correspond to the instruction.
 2. The ''decoder output'' goes before the decode function in the same source file (decoder.cc). This output typically contains definitions that do not need to be visible to the `execute()` methods: inline constructor definitions, non-inline method definitions (e.g., for disassembly), etc.
 3. The ''exec output'' contains per-CPU model definitions, i.e., the `execute()` methods for the instruction class.
 4. The ''decode block'' contains a statement or block of statements that go into the decode function (in the body of the corresponding case statement). These statements take control once the bit pattern specified by the decode block is recognized, and are responsible for returning an appropriate instruction object.

The syntax for defining an instruction format is as follows:

{% raw %}
```
def format FormatName(arg1, arg2) {{
    [code omitted]
}};
```
{% endraw %}

In this example, the format is named "FormatName". (By convention, instruction format names begin with a capital letter and use mixed case.) Instruction definitions using this format will be expected to provide two arguments (`arg1` and `arg2`). The language also supports the Python variable-argument mechanism: if the final parameter begins with an asterisk (e.g., `*rest`), it receives a list of all the otherwise unbound arguments from the call site.

Note that the next-to-last syntactic token in the format definition (prior to the semicolon) is simply a code literal (string constant), as described above. In this case, the text within the code literal is a Python code block. This Python code will be called at each instruction definition that uses the specified format.

In addition to the explicit arguments, the Python code is supplied with two additional parameters: `name`, which is bound to the instruction mnemonic, and `Name`, which is the mnemonic with the first letter capitalized (useful for forming C++ class names based on the mnemonic).

The format code block specifies the generated code by assigning strings to four special variables: `header_output`, `decoder_output`, `exec_output`, and `decode_block`. Assignment is optional; for any of these variables that does not receive a value, no code will be generated for the corresponding section. These strings may be generated by whatever method is convenient. In practice, nearly all instruction formats use the support functions provided by the ISA description parser to specialize code templates based on characteristics extracted automatically from C-like code snippets. Discussion of these features is deferred to the [Code parsing](#code-parsing) page.

Although the ISA description is completely independent of any specific simulator CPU model, some C++ code (particularly the exec output) must be specialized slightly for each model. This specialization is handled by automatic substitution of CPU-model-specific symbols. These symbols start with `CPU_` and are treated specially by the parser. Currently there is only one model-specific symbol, `CPU_exec_context`, which evaluates to the model's execution context class name. As with templates (see [Template definitions](#template-definitions)), references to CPU-specific symbols use Python key-based format strings; a reference to the `CPU_exec_context` symbol thus appears in a string as `%(CPU_exec_context)s`.

If a string assigned to `header_output`, `decoder_output`, or `decode_block` contains a CPU-specific symbol reference, the string is replicated once for each CPU model, and each instance has its CPU-specific symbols substituted according to that model. The resulting strings are then concatenated to form the final output. Strings assigned to `exec_output` are always replicated and subsituted once for each CPU model, regardless of whether they contain CPU-specific symbol references. The instances are not concatenated, but are tracked separately, and are placed in separate per-CPU-model files (e.g., simple\_cpu\_exec.cc).

### Template definitions

As discussed in section Format definitions above, the purpose of an instruction format is to process the arguments of an instruction definition and generate several pieces of C++ code. These code pieces are usually generated by specializing a code template. The description language provides a simple syntax for defining these templates: the keywords `def template`, the template name, the template body (a code literal), and a semicolon. By convention, template names start with a capital letter, use mixed case, and end with "Declare" (for declaration (header output) templates), "Decode" (for decode-block templates), "Constructor" (for decoder output templates), or "Execute" (for exec output templates).
For example, the simplest useful decode template is as follows:

{% raw %}
```
def template BasicDecode {{
    return new %(class_name)s(machInst);
}};
```
{% endraw %}

An instruction format would specialize this template for a particular instruction by substituting the actual class name for `%(class_name)s`. (Template specialization relies on the Python string format operator `%`. The term `%(class_name)s` is an extension of the C `%s` format string indicating that the value of the symbol `class_name` should be substituted.) The resulting code would then cause the C++ decode function to create a new object of the specified class when the particular instruction was recognized.

Templates are represented in the parser as Python objects. A template is used to generate a string typically by calling the template object's `subst()` method. This method takes a single argument that specifies the mapping of substitution symbols in the template (e.g., `%(class_name)s`) to specific values. If the argument is a dictionary, the dictionary itself specifies the mapping. Otherwise, the argument must be another Python object, and the object's attributes are used as the mapping. In practice, the argument to `subst()` is nearly always an instance of the parser's InstObjParams class; see the [InstObjParams class](#the-instobjparams-class). A template may also reference other templates (e.g., `%(BasicDecode)s`) in addition to symbols specified by the `subst()` argument; these will be interpolated into the result by `subst()` as well.

Template references to CPU-model-specific symbols (see [Format definitions](#format-definitions)) are not expanded by `subst()`, but are passed through intact. This feature allows them to later be expanded appropriately according to whether the result is assigned to `exec_output` or another output section. However, when a template containing a CPU-model-specific symbol is referenced by another template, then the former template is replicated and expanded into a single string before interpolation, as with templates assigned to `header_output` or `decoder_output`. This policy guarantees that only templates directly containing CPU-model-specific symbols will be replicated, never templates that contain such symbols indirectly. This last feature is used to interpolate per-CPU declarations of the `execute()` method into the instruction class declaration template (see the `BasicExecDeclare` template in the Alpha ISA description).

### Output blocks

Output blocks allow the ISA description to include C++ code that is copied nearly verbatim to the output file. These blocks are useful for defining classes and local functions that are shared among multiple instruction objects. An output block has the following format:

{% raw %}
```
output <destination> {{
    [code omitted]
}};
```
{% endraw %}

The `<destination>` keyword must be one of `header`, `decoder`, or `exec`. The code within the code literal is treated as if it were assigned to the `header_output` `decoder_output`, or `exec_output` variable within an instruction format, respectively, including the special processing of CPU-model-specific symbols. The only additional processing performed on the code literal is substitution of bitfield operators, as used in instruction definitions (see [Bitfield operators](#bitfield-operators), and interpolation of references to templates.

### Let blocks

Let blocks provide for global Python code. These blocks consist simply of the keyword `let` followed by a code literal (double-brace delimited string) and a semicolon.
The code literal is executed immediately by the Python interpreter. The parser maintains the execution context across let blocks, so that variables and functions defined in one let block will be accessible in subsequent let blocks. This context is also used when executing instruction format definitions. The primary purpose of let blocks is to define shared Python data structures and functions for use in instruction formats. The parser exports a limited set of definitions into this execution context, including the set of defined templates (see [Template definitions](#template-definitions), the `InstObjParams` and `CodeBlock` classes (see [Code parsing](#code-parsing)), and the standard Python `string` and `re` (regular expression) modules.

### Bitfield definitions

A bitfield definition provides a name for a bitfield within a machine instruction. These names are typically used as the bitfield specifications in decode blocks. The names are also used within other C++ code in the decoder file, including instruction class definitions and decode code.
The bitfield definition syntax is demonstrated in these examples:

```
def bitfield OPCODE <31:26>;
def bitfield IMM <12>;
def signed bitfield MEMDISP <15:0>;
```

The specified bit range is inclusive on both ends, and bit 0 is the least significant bit; thus the OPCODE bitfield in the example extracts the most significant six bits from a 32-bit instruction. A single index value extracts a one-bit field, IMM. The extracted value is zero-extended by default; with the additional signed keyword, as in the MEMDISP example, the extracted value will be sign extended. The implementation of bitfields is based on preprocessor macros and C++ template functions, so the size of the resulting value will depend on the context.

To fully understand where bitfield definitions can be used, we need to go under the hood a bit. A bitfield definition simply generates a C++ preprocessor macro that extracts the specified bitfield from the implicit variable `machInst`. The machine instruction parameter to the decode function is also called `machInst`; thus any use of a bitfield name that ends up inside the decode function (such as the argument of a decode block or the decode piece of an instruction format's output) will implicitly reference the instruction currently being decoded. The binary machine instruction stored in the `StaticInst` object is also named `machInst`, so any use of a bitfield name in a member function of an instruction object will reference this stored value. This data member is initialized in the `StaticInst` constructor, so it is safe to use bitfield names even in the constructors of derived objects.

### Operand and operand type definitions

These statements specify the operand types that can be used in the code blocks that express the functional operation of instructions. See [Operand type qualifiers](#operand-type-qualifiers)  and [Instruction parsing](#instruction-operands).

### Namespace declaration

The final component of the declaration section is the namespace declaration, consisting of the keyword `namespace` followed by an identifier and a semicolon. Exactly one namespace declaration must appear in the declarations section. The resulting C++ decode function, the declarations resulting from the instruction definitions in the decode block, and the contents of any `declare` statements occurring after then namespace declaration will be placed in a C++ namespace with the specified name. The contents of `declare` statements occurring before the namespace declaration will be outside the namespace.


## ISA parser

### Formats

### operands

### decode tree

### let blocks

### microcode assembler
#### microops
#### macroops
#### directives
#### rom object

### Lots more stuff

# Code parsing

To a large extent, the power and flexibility of the ISA description mechanism stem from the fact that the mapping from a brief instruction definition provided in the decode block to the resulting C++ code is performed in a general-purpose programming language (Python). (This function is performed by the "instruction format" definition described above in [Format definitions](#format-definitions). Technically, the ISA description language allows any arbitrary Python code to perform this mapping. However, the parser provides a library of Python classes and functions designed to automate the process of deducing an instruction's characteristics from a brief description of its operation, and generating the strings required to populate declaration and decode templates. This library represents roughly half of the code in isa\_parser.py.

Instruction behaviors are described using C++ with two extensions: bitfield operators and operand type qualifiers. To avoid building a full C++ parser into the ISA description system (or conversely constraining the C++ that could be used for instruction descriptions), these extensions are implemented using regular expression matching and substitution. As a result, there are some syntactic constraints on their usage. The following two sections discuss these extensions in turn. The third section discusses operand parsing, the technique by which the parser automatically infers most instruction characteristics. The final two sections discuss the Python classes through which instruction formats interact with the library: `CodeBlock`, which analyzes and encapsulates instruction description code; and the instruction object parameter class, `InstObjParams`, which encapsulates the full set of parameters to be substituted into a template.

### Bitfield operators

Simple bitfield extraction can be performed on rvalues using the `<:>` postfix operator. Bit numbering matches that used in global bitfield definitions (see [Bitfield definitions](#bitfield-definitions)). For example, `Ra<7:0>` extracts the low 8 bits of register `Ra`. Single-bit fields can be specified by eliminating the latter operand, e.g. `Rb<31:>`. Unlike in global bitfield definitions, the colon cannot be eliminated, as it becomes too difficult to distinguish bitfield operators from template arguments. In addition, the bit index parameters must be either identifiers or integer constants; expressions are not allowed. The bit operator will apply either to the syntactic token on its left, or, if that token is a closing parenthesis, to the parenthesized expression.

### Operand type qualifiers

The effective type of an instruction operand (e.g., a register) may be specified by appending a period and a type qualifier to the operand name. The list of type qualifiers is architecture-specific; the `def operand_types` statement in the ISA description is used to specify it. The specification is in the form of a Python dictionary which maps a type extension to type name. For example, the Alpha ISA definition is as follows:

{% raw %}
```
def operand_types {{
    'sb' : 'int8_t',
    'ub' : 'uint8_t',
    'sw' : 'int16_t',
    'uw' : 'uint16_t',
    'sl' : 'int32_t',
    'ul' : 'uint32_t',
    'sq' : 'int64_t',
    'uq' : 'uint64_t',
    'sf' : 'float',
    'df' : 'double'
}};
```
{% endraw %}

Thus the Alpha 32-bit add instruction addl could be defined as:
```
Rc.sl = Ra.sl + Rb.sl;
```
The operations are performed using the types specified; the result will be converted from the specified type to the appropriate register value (in this case by sign-extending the 32-bit result to 64 bits, since Alpha integer registers are 64 bits in size).

Type qualifiers are allowed only on recognized instruction operands (see [Instruction operands](#instruction-operands)).

### Instruction operands

Most of the automation provided by the parser is based on its recognition of the operands used in the instruction definition code. Most relevant instruction characteristics can be inferred from the operands: floating-point vs. integer instructions can be recognized by the registers used, an instruction that reads from a memory location is a load, etc. In combination with the bitfield operands and type qualifiers described above, most instructions can be described in a single line of code. In addition, most of the differences between simulator CPU models lies in the operand access mechanisms; by generating the code for these accesses automatically, a single description suffices for a variety of situations.

The ISA description provides a list of recognized instruction operands and their characteristics via the `def operands` statement. This statement specifies a Python dictionary that maps operand strings to a five-element tuple.  The elements of the tuple specify the operand as follows:

1. the operand class, which must be one of the strings "IntReg", "FloatReg", "Mem", "NPC", or "ControlReg", indicating an integer register, floating-point register, memory location, the next program counter (NPC), or a control register, respectively. 
2. the default type of the operand (an extension string defined in the `def operand_types` block),
3. a specifier indicating how specific instances of the operand are decoded (e.g., a bitfield name),
4. a string or triple of strings indicating the instruction flags that can be inferred when the operand is used, and
5. a sort priority used to control the order of operands in disassembly.

For example, a simplified subset of the Alpha ISA operand traits map is as follows:

{% raw %}
```
def operands {{
    'Ra': ('IntReg', 'uq', 'RA', 'IsInteger', 1),
    'Rb': ('IntReg', 'uq', 'RB', 'IsInteger', 2),
    'Rc': ('IntReg', 'uq', 'RC', 'IsInteger', 3),
    'Fa': ('FloatReg', 'df', 'FA', 'IsFloating', 1),
    'Fb': ('FloatReg', 'df', 'FB', 'IsFloating', 2),
    'Fc': ('FloatReg', 'df', 'FC', 'IsFloating', 3),
    'Mem': ('Mem', 'uq', None, ('IsMemRef', 'IsLoad', 'IsStore'), 4),
    'NPC': ('NPC', 'uq', None, ( None, None, 'IsControl'), 4)
}};
```
{% endraw %}

The operand named `Ra` is an integer register, default type `uq` (unsigned quadword), uses the `RA` bitfield from the instruction, implies the `IsInteger` instruction flag, and has a sort priority of 1 (placing it first in any list of operands).

For the instruction flag element, a single string (such as `'IsInteger'` implies an unconditionally inferred instruction flag. If the flag operand is a triple, the first element is unconditional, the second is inferred when the operand is a source, and the third when it is a destination. Thus the `('IsMemRef', 'IsLoad', 'IsStore')` element for memory references indicates that any instruction with a memory operand is marked as a memory reference. In addition, if the memory operand is a source, the instruction is marked as a load, while if the operand is a destination, the instruction is marked a store. Similarly, the `(None, None, 'IsControl')` tuple for the NPC operand indicates that any instruction that writes to the NPC is a control instruction, but instructions which merely reference NPC as a source do not receive any default flags.

Note that description code parsing uses regular expressions, which limits the ability of the parser to infer the nature of a partciular operand.  In particular, destination operands are distinguished from source operands solely by testing whether the operand appears on the left-hand side of an assignment operator (`=`). Destination operands that are assigned to in a different fashion, e.g. by being passed by reference to other functions, must still appear on the left-hand side of an assignment to be properly recognized as destinations.  The parser also does not recognize C compound assignments, e.g., `+=`.  If an operand is both a source and a destination, it must appear on both the left- and right-hand sides of `=`.

Another limitation of regular-expression-based code parsing is that control flow in the code block is not recognized.  Combined with the details of how register updates are performed in the CPU models, this means that destinations cannot be updated conditionally.  If a particular register is recognized as a destination register, that register will always be updated at the end of the `execute()` method, and thus the code must assign a valid value to that register along each possible code path within the block.

### The CodeBlock class

An instruction format requests processing of a string containing instruction description code by passing the string to the CodeBlock constructor. The constructor performs all of the needed analysis and processing, storing the results in the returned object. Among the CodeBlock fields are:

* `orig_code`: the original code string.
* `code`: a processed string containing legal C++ code, derived from the original code by substituting in the bitfield operators and munging operand type qualifiers (s/\./\_/) to make valid C++ identifiers.
* `constructor`: code for the constructor of an instruction object, initializing various C++ object fields including the number of operands and the register indices of the operands.
* `exec_decl`: code to declare the C++ variables corresponding to the operands, for use in an execution emulation function.
* `*_rd`: code to read the actual operand values into the corresponding C++ variables for source operands. The first part of the name indicates the relevant CPU model (currently simple and dtld are supported).
* `*_wb`: code to write the C++ variable contents back to the appropriate register or memory location. Again, the first part of the name reflects the CPU model.
* `*_mem_rd`, `*_nonmem_rd`, `*_mem_wb`, `*_nonmem_wb`: as above, but with memory and non-memory operands segregated.
* `flags`: the set of instruction flags implied by the operands.
* `op_class`: a basic guess at the instruction's operation class (see OpClass) based on the operand types alone.

### The InstObjParams class

Instances of the InstObjParams class encapsulate all of the parameters needed to substitute into a code template, to be used as the argument to a template's `subst()` method (see Template definitions). 

```python
class InstObjParams(object):
    def __init___(self, parser, 
                  mem, class_name, base_class = '',
                  snippets = {}, opt_args = []):
```

The first three constructor arguments populate the object's `mnemonic`, `class_name`, and (optionally) `base_class` members. The fourth (optional) argument is a CodeBlock object; all of the members of the provided CodeBlock object are copied to the new object, making them accessible for template substitution. Any remaining arguments are interpreted as either additional instruction flags (appended to the `flags` list inherited from the CodeBlock argument, if any), or as an operation class (overriding any `op_class` from the CodeBlock).

