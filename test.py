from ELFPatch import ELFPatch 

f = ELFPatch(b"./test")

new_patch = f.new_patch(virtual_address=f.elf.ehdr.e_entry, size=0x100, append_original_instructions=True, append_jump_back=True)

new_patch.update_patch(f.assembler.assemble("""
mov rax, 0x1
mov rdi, 0x1
jmp get_str

make_syscall:
pop rsi
mov rdx, 12
syscall
jmp end

get_str:
call make_syscall
.string "SICED PATCH\n"

end:
xor rax, rax
xor rdi, rdi
xor rsi, rsi
xor rdx, rdx
"""))

# new_patch.update_patch(b"\x48\xC7\xC0\x01\x00\x00\x00\x48\xC7\xC7\x01\x00\x00\x00\xEB\x0C\x5E\x48\xC7\xC2\x0C\x00\x00\x00\x0F\x05\xEB\x12\xE8\xEF\xFF\xFF\xFF\x53\x49\x43\x45\x44\x20\x50\x41\x54\x43\x48\x0A\x00")



print("New Patch at", hex(new_patch.chunk.virtual_address))
f.write_file("./out")
