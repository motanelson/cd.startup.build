; hello.asm
[BITS 16]          ; Configuração para 16 bits (modo real)
[ORG 0x7C00]       ; Define o endereço de carregamento

start:
    mov ah, 0x0E    ; Função de imprimir caractere do BIOS
    mov si, msg     ; Ponteiro para a mensagem

.print_char:
    lodsb           ; Carrega o próximo byte de [SI] para AL
    or al, al       ; Verifica se é o fim da string (0)
    jz .hang        ; Se sim, termina
    int 0x10        ; Chama o BIOS para imprimir
    jmp .print_char ; Continua imprimindo

.hang:
    cli             ; Desabilita interrupções
    hlt             ; Entra em estado de espera

msg db "Hello, World!", 0 ; Mensagem a ser impressa (terminada em 0)

times 510-($-$$) db 0 ; Preenche até 510 bytes
dw 0xAA55             ; Assinatura do setor de boot (0xAA55)