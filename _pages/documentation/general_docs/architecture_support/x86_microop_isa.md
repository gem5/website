---
layout: documentation
title: X86 Micro-op ISA
doc: gem5 documentation
parent: architecture_support
permalink: documentation/general_docs/architecture_support/x86_microop_isa/
---

# Register Ops
These microops typically take two sources and produce one result. Most have a version that operates on only registers and a version which operates on registers and an immediate value. Some optionally set flags according to their operation. Some of them can be predicated. 

### Add
Addition.

#### add Dest, Src1, Src2
Dest # Dest <- Src1 + Src2

Adds the contents of the Src1 and Src2 registers and puts the result in the Dest register.

#### addi Dest, Src1, Imm
Dest # Dest <- Src1 + Imm

Adds the contents of the Src1 register and the immediate Imm and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The carry out of the most significant bit.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | The carry from the fourth to fifth bit positions.
SF	   | The sign of the result.
OF	   | Whether there was an overflow.

### Adc
Add with carry.

#### adc Dest, Src1, Src2
Dest # Dest <- Src1 + Src2 + CF

Adds the contents of the Src1 and Src2 registers and the carry flag and puts the result in the Dest register.

#### adci Dest, Src1, Imm
Dest # Dest <- Src1 + Imm + CF

Adds the contents of the Src1 register, the immediate Imm, and the carry flag and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The carry out of the most significant bit.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | The carry from the fourth to fifth bit positions.
SF	   | The sign of the result.
OF	   | Whether there was an overflow.

### Sub
Subtraction.

#### sub Dest, Src1, Src2
Dest # Dest <- Src1 - Src2

Subtracts the contents of the Src2 register from the Src1 register and puts the result in the Dest register.

#### subi Dest, Src1, Imm
Dest # Dest <- Src1 - Imm

Subtracts the contents of the immediate Imm from the Src1 register and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The borrow into of the most significant bit.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | The borrow from the fourth to fifth bit positions.
SF	   | The sign of the result.
OF	   | Whether there was an overflow.

### Sbb

Subtract with borrow.

#### sbb Dest, Src1, Src2
Dest # Dest <- Src1 - Src2 - CF

Subtracts the contents of the Src2 register and the carry flag from the Src1 register and puts the result in the Dest register.

#### sbbi Dest, Src1, Imm
Dest # Dest <- Src1 - Imm - CF

Subtracts the immediate Imm and the carry flag from the Src1 register and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The borrow into of the most significant bit.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | The borrow from the fourth to fifth bit positions.
SF	   | The sign of the result.
OF	   | Whether there was an overflow.

### Mul1s

Signed multiply.

#### mul1s Src1, Src2
ProdHi:ProdLo # Src1 * Src2

Multiplies the unsigned contents of the Src1 and Src2 registers and puts the high and low portions of the product into the internal registers ProdHi and ProdLo, respectively.

#### mul1si Src1, Imm
ProdHi:ProdLo # Src1 * Imm

Multiplies the unsigned contents of the Src1 register and the immediate Imm and puts the high and low portions of the product into the internal registers ProdHi and ProdLo, respectively.

#### Flags
This microop does not set any flags.

### Mul1u

Unsigned multiply.

#### mul1u Src1, Src2
ProdHi:ProdLo # Src1 * Src2

Multiplies the unsigned contents of the Src1 and Src2 registers and puts the high and low portions of the product into the internal registers ProdHi and ProdLo, respectively.

#### mul1ui Src1, Imm
ProdHi:ProdLo # Src1 * Imm

Multiplies the unsigned contents of the Src1 register and the immediate Imm and puts the high and low portions of the product into the internal registers ProdHi and ProdLo, respectively.

#### Flags
This microop does not set any flags.

### Mulel

Unload multiply result low.

#### mulel Dest
Dest # Dest <- ProdLo

Moves the value of the internal ProdLo register into the Dest register.

#### Flags
This microop does not set any flags.

### Muleh

Unload multiply result high.

#### muleh Dest
Dest # Dest <- ProdHi

Moves the value of the internal ProdHi register into the Dest register.

#### Flags
This microop optionally sets the CF, ECF, and OF flags.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | Whether ProdHi is non-zero.
OF	   | Whether ProdHi is zero.

### Div1

First stage of division.

#### div1 Src1, Src2
Quotient * Src2 + Remainder # Src1
Divisor # Src2

Begins a division operation where the contents of SrcReg1 is the high part of the dividend and the contents of SrcReg2 is the divisor. The remainder from this partial division is put in the internal register Remainder. The quotient is put in the internal register Quotient. The divisor is put in the internal register Divisor.

#### div1i Src1, Imm:
Quotient * Imm + Remainder # Src1
Divisor # Imm

Begins a division operation where the contents of SrcReg1 is the high part of the dividend and the immediate Imm is the divisor. The remainder from this partial division is put in the internal register Remainder. The quotient is put in the internal register Quotient. The divisor is put in the internal register Divisor.

#### Flags
This microop does not set any flags.

### Div2

Second and later stages of division.

#### div2 Dest, Src1, Src2
Quotient * Divisor + Remainder # original Remainder with bits shifted in from Src1

Dest # Dest <- Src2 - number of bits shifted in above

Performs subsequent steps of division following a div1 instruction. The contents of the register Src1 is the low portion of the dividend. The contents of the register Src2 denote the number of bits in Src1 that have not yet been used before this step in the division. Dest is set to the number of bits in Src1 that have not been used after this step. The internal registers Quotient, Divisor, and Remainder are updated by this instruction.

If there are no remaining bits in Src1, this instruction does nothing except optionally compute flags.

#### div2i Dest, Src1, Imm
Quotient * Divisor + Remainder # original Remainder with bits shifted in from Src1

Dest # Dest <- Imm - number of bits shifted in above

Performs subsequent steps of division following a div1 instruction. The contents of the register Src1 is the low portion of the dividend. The immediate Imm denotes the number of bits in Src1 that have not yet been used before this step in the division. Dest is set to the number of bits in Src1 that have not been used after this step. The internal registers Quotient, Divisor, and Remainder are updated by this instruction.

If there are no remaining bits in Src1, this instruction does nothing except optionally compute flags.

#### Flags
This microop optionally sets the EZF flag.

Flag       | Meaning
---------- | ------------------------------------------
EZF	   | Whether there are any remaining bits in Src1 after this step.

### Divq

Unload division quotient.

#### divq Dest
Dest # Dest <- Quotient

Moves the value of the internal Quotient register into the Dest register.

#### Flags
This microop does not set any flags.

### Divr

Unload division remainder.

#### divr Dest
Dest # Dest <- Remainder

Moves the value of the internal Remainder register into the Dest register.

#### Flags
This microop does not set any flags.

### Or

Logical or.

#### or Dest, Src1, Src2
Dest # Dest <- Src1 | Src2

Computes the bitwise or of the contents of the Src1 and Src2 registers and puts the result in the Dest register.

#### ori Dest, Src1, Imm
Dest # Dest <- Src1 | Imm

Computes the bitwise or of the contents of the Src1 register and the immediate Imm and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.
There is nothing that prevents computing a value for the AF flag, but it's value will be meaningless.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | Cleared.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | Undefined.
SF	   | The sign of the result.
OF	   | Cleared.

### And

Logical And

#### and Dest, Src1, Src2
Dest # Dest <- Src1 & Src2

Computes the bitwise and of the contents of the Src1 and Src2 registers and puts the result in the Dest register.

#### andi Dest, Src1, Imm
Dest # Dest <- Src1 & Imm

Computes the bitwise and of the contents of the Src1 register and the immediate Imm and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.
There is nothing that prevents computing a value for the AF flag, but it's value will be meaningless.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | Cleared.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | Undefined.
SF	   | The sign of the result.
OF	   | Cleared.

### Xor

Logical exclusive or.

#### xor Dest, Src1, Src2
Dest # Dest <- Src1 | Src2

Computes the bitwise xor of the contents of the Src1 and Src2 registers and puts the result in the Dest register.

#### xori Dest, Src1, Imm
Dest # Dest <- Src1 | Imm

Computes the bitwise xor of the contents of the Src1 register and the immediate Imm and puts the result in the Dest register.

#### Flags
This microop optionally sets the CF, ECF, ZF, EZF, PF, AF, SF, and OF flags.
There is nothing that prevents computing a value for the AF flag, but it's value will be meaningless.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | Cleared.
ZF and EZF | Whether the result was zero.
PF         | The parity of the result.
AF         | Undefined.
SF	   | The sign of the result.
OF	   | Cleared.

### Sll

Logical left shift.

#### sll Dest, Src1, Src2
Dest # Dest <- Src1 << Src2

Shifts the contents of the Src1 register to the left by the value in the Src2 register and writes the result into the Dest register. The shift amount is truncated to either 5 or 6 bits, depending on the operand size. 

#### slli Dest, Src1, Imm
Dest # Dest <- Src1 << Imm

Shifts the contents of the Src1 register to the left by the value in the immediate Imm and writes the result into the Dest register. The shift amount is truncated to either 5 or 6 bits, depending on the operand size.

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the shift amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The last bit shifted out of the result.
OF	   | The exclusive OR of what this instruction would set the CF flag to, if requested, and the most significant bit of the result.

### Srl

Logical right shift.

#### srl Dest, Src1, Src2
Dest # Dest <- Src1 >>(logical) Src2

Shifts the contents of the Src1 register to the right by the value in the Src2 register and writes the result into the Dest register. Bits which are shifted in sign extend the result. The shift amount is truncated to either 5 or 6 bits, depending on the operand size. 

#### srli Dest, Src1, Imm
Dest # Dest <- Src1 >>(logical) Imm

Shifts the contents of the Src1 register to the right by the value in the immediate Imm and writes the result into the Dest register. Bits which are shifted in sign extend the result. The shift amount is truncated to either 5 or 6 bits, depending on the operand size. 

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the shift amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The last bit shifted out of the result.
SF	   | The most significant bit of the original value to shift.

### Sra

Arithmetic right shift.

#### sra Dest, Src1, Src2
Dest # Dest <- Src1 >>(arithmetic) Src2

Shifts the contents of the Src1 register to the right by the value in the Src2 register and writes the result into the Dest register. Bits which are shifted in zero extend the result. The shift amount is truncated to either 5 or 6 bits, depending on the operand size. 

#### srai Dest, Src1, Imm
Dest # Dest <- Src1 >>(arithmetic) Imm

Shifts the contents of the Src1 register to the right by the value in the immediate Imm and writes the result into the Dest register. Bits which are shifted in zero extend the result. The shift amount is truncated to either 5 or 6 bits, depending on the operand size. 

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the shift amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The last bit shifted out of the result.
OF	   | Cleared.

### Ror

Rotate right.

#### ror Dest, Src1, Src2
Rotates the contents of the Src1 register to the right by the value in the Src2 register and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### rori Dest, Src1, Imm
Rotates the contents of the Src1 register to the right by the value in the immediate Imm and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the rotate amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The most significant bit of the result.
OF	   | The exclusive OR of the most two significant bits of the original value.

### Rcr

Rotate right through carry.

#### rcr Dest, Src1, Src2
Rotates the contents of the Src1 register through the carry flag and to the right by the value in the Src2 register and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### rcri Dest, Src1, Imm
Rotates the contents of the Src1 register through the carry flag and to the right by the value in the immediate Imm and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the rotate amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The last bit shifted out of the result.
OF	   | The exclusive OR of the CF flag before the rotate and the most significant bit of the original value.

### Rol

Rotate left.

#### rol Dest, Src1, Src2
Rotates the contents of the Src1 register to the left by the value in the Src2 register and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### roli Dest, Src1, Imm
Rotates the contents of the Src1 register to the left by the value in the immediate Imm and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the rotate amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The least significant bit of the result.
OF	   | The exclusive OR of the most and least significant bits of the result.

### Rcl

Rotate left through carry.

#### rcl Dest, Src1, Src2
Rotates the contents of the Src1 register through the carry flag and to the left by the value in the Src2 register and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### rcli Dest, Src1, Imm
Rotates the contents of the Src1 register through the carry flag and to the left by the value in the immediate Imm and writes the result into the Dest register. The rotate amount is truncated to either 5 or 6 bits, depending on the operand size.

#### Flags
This microop optionally sets the CF, ECF, and OF flags. If the rotate amount is zero, no flags are modified.

Flag       | Meaning
---------- | ------------------------------------------
CF and ECF | The last bit rotated out of the result.
OF	   | The exclusive OR of CF before the rotate and the most significant bit of the result.

### Mov

Move.

#### mov Dest, Src1, Src2
Dest # Src1 <- Src2

Merge the contents of the Src2 register into the contents of Src1 and put the result into the Dest register.

#### movi Dest, Src1, Imm
Dest # Src1 <- Imm

Merge the contents of the immediate Imm into the contents of Src1 and put the results into the Dest register.

#### Flags
This microop does not set any flags. It is optionally predicated.

### Sext

Sign extend.

#### sext Dest, Src1, Imm
Dest # Dest <- sign_extend(Src1, Imm)

Sign extend the value in the Src1 register starting at the bit position in the immediate Imm, and put the result in the Dest register.

#### Flags
This microop does not set any flags.

### Zext

Zero extend.

#### zext Dest, Src1, Imm
Dest # Dest <- zero_extend(Src1, Imm)

Zero extend the value in the Src1 register starting at the bit position in the immediate Imm, and put the result in the Dest register.

#### Flags
This microop does not set any flags.

### Ruflag

Read user flag.

#### ruflag Dest, Imm
Reads the user level flag stored in the bit position specified by the immediate Imm and stores it in the register Dest.

The mapping between values of Imm and user level flags is show in the following table.

Imm        | Flag
---------- | ------------------------------------------
0          | CF (carry flag)
2          | PF (parity flag)
3          | ECF (emulation carry flag)
4          | AF (auxiliary flag)
5          | EZF (emulation zero flag)
6          | ZF (zero flag)
7          | CF (sign flag)
10         | CF (direction flag)
11         | CF (overflow flag)

#### Flags
The EZF flag is always set. In the future this may become optional.


### Ruflags

Read all user flags.

#### ruflags Dest
Dest # user flags

Store the user level flags into the Dest register.

#### Flags
This microop does not set any flags.

### Wruflags

Write all user flags.

#### wruflags Src1, Src2
user flags # Src1 ^ Src2

Set the user level flags to the exclusive or of the Src1 and Src2 registers.

#### wruflagsi Src1, Imm
user flags # Src1 ^ Imm

Set the user level flags to the exclusive or of the Src1 register and the immediate Imm.

#### Flags
See above.

### Rdip

Read the instruction pointer.

#### rdip Dest
Dest # rIP

Set the Dest register to the current value of rIP.

#### Flags
This microop does not set any flags.

### Wrip

Write the instruction pointer.

#### wrip Src1, Src2
rIP # Src1 + Src2

Set the rIP to the sum of the Src1 and Src2 registers. This causes a macroop branch at the end of the current macroop.

#### wripi Src1, Imm
micropc # Src1 + Imm

Set the rIP to the sum of the Src1 register and immediate Imm. This causes a macroop branch at the end of the current macroop.

#### Flags
This microop does not set any flags. It is optionally predicated.

### Chks
Check selector.

Not yet implemented.

# Load/Store Ops

### Ld
Load.
#### ld Data, Seg, Sib, Disp
Loads the integer register Data from memory.

### Ldf
Load floating point.
#### ldf Data, Seg, Sib, Disp
Loads the floating point register Data from memory.

### Ldm
Load multimedia.
#### ldm Data, Seg, Sib, Disp
Load the multimedia register Data from memory.
This is not implemented and may never be.

### Ldst
Load with store check.
#### Ldst Data, Seg, Sib, Disp
Load the integer register Data from memory while also checking if a store to that location would succeed.
This is not implemented currently.

### Ldstl
Load with store check, locked.
#### Ldst Data, Seg, Sib, Disp
Load the integer register Data from memory while also checking if a store to that location would succeed, and also provide the semantics of the "LOCK" instruction prefix.
This is not implemented currently.

### St
Store.
#### st Data, Seg, Sib, Disp
Stores the integer register Data to memory.

### Stf
Store floating point.
#### stf Data, Seg, Sib, Disp
Stores the floating point register Data to memory.

### Stm
Store multimedia.
#### stm Data, Seg, Sib, Disp
Store the multimedia register Data to memory.
This is not implemented and may never be.

### Stupd
Store with base update.
#### Stupd Data, Seg, Sib, Disp
Store the integer register Data to memory and update the base register.

### Lea
Load effective address.
#### lea Data, Seg, Sib, Disp
Calculates the address for this combination of parameters and stores it in Data.

### Cda
Check data address.
#### cda Seg, Sib, Disp
Check whether the data address is valid.
This is not implemented currently.

### Cdaf
CDA with cache line flush.
#### cdaf Seg, Sib, Disp
Check whether the data address is valid, and flush cache lines
This is not implemented currently.

### Cia
Check instruction address.
#### cia Seg, Sib, Disp
Check whether the instruction address is valid.
This is not implemented currently.

### Tia
TLB invalidate address
#### tia Seg, Sib, Disp
Invalidate the tlb entry which corresponds to this address.
This is not implemented currently.

# Load immediate Op

### Limm
#### limm Dest, Imm
Stores the 64 bit immediate Imm into the integer register Dest.

# Floating Point Ops

### Movfp
#### movfp Dest, Src
Dest # Src

Move the contents of the floating point register Src into the floating point register Dest.

This instruction is predicated.

### Xorfp
#### xorfp Dest, Src1, Src2
Dest # Src1 ^ Src2

Compute the bitwise exclusive or of the floating point registers Src1 and Src2 and put the result in the floating point register Dest.

### Sqrtfp
#### sqrtfp Dest, Src
Dest # sqrt(Src)

Compute the square root of the floating point register Src and put the result in floating point register Dest.

### Addfp
#### addfp Dest, Src1, Src2
Dest # Src1 + Src2

Compute the sum of the floating point registers Src1 and Src2 and put the result in the floating point register Dest.

### Subfp
#### subfp Dest, Src1, Src2
Dest # Src1 - Src2

Compute the difference of the floating point registers Src1 and Src2 and put the result in the floating point register Dest.

### Mulfp
#### mulfp Dest, Src1, Src2
Dest # Src1 * Src2

Compute the product of the floating point registers Src1 and Src2 and put the result in the floating point register Dest.

### Divfp
#### divfp Dest, Src1, Src2
Dest # Src1 / Src2

Divide Src1 by Src2 and put the result in the floating point register Dest.

### Compfp
#### compfp Src1, Src2
Compare floating point registers Src1 and Src2.

### Cvtf_i2d
#### cvtf_i2d Dest, Src
Convert integer register Src into a double floating point value and store the result in the lower part of Dest.

### Cvtf_i2d_hi
#### cvtf_i2d_hi Dest, Src
Convert integer register Src into a double floating point value and store the result in the upper part of Dest.

### Cvtf_d2i
#### cvtf_d2i Dest, Src
Convert floating point register Src into an integer value and store the result in the integer register Dest.

# Special Ops

### Fault
Generate a fault.
#### fault fault_code
Uses the C++ code fault_code to allocate a Fault object to return.

### Lddha
Set the default handler for a fault.
This is not implemented currently.

### Ldaha
Set the alternate handler for a fault
This is not implemented currently.

# Sequencing Ops
These microops are used for control flow withing microcode

### Br

Microcode branch. This is never considered the last microop of a sequence. If it appears at the end of a macroop, it is assumed that it branches to microcode in the ROM.

#### br target
micropc # target

Set the micropc to the 16 bit immediate target.

#### Flags
This microop does not set any flags. It is optionally predicated.

### Eret

Return from emulation. This instruction is always considered the last microop in a sequence. When executing from the ROM, it is the only way to return to normal instruction decoding.

#### eret

Return from emulation.

#### Flags
This microop does not set any flags. It is optionally predicated.
