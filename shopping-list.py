lista_de_compras = []

def adicionar_item():
    nome = input("Digite o nome do item: ")
    preco = float(input("Digite o preço do item: "))
    quantidade = int(input("Digite a quantidade do item: "))
    item = {"nome": nome, "preco": preco, "quantidade": quantidade}
    lista_de_compras.append(item)
    if quantidade > 1:
        print(f"{quantidade} unidades de {nome} foram adicionadas à lista de compras.")
    else:
        print(f"{nome} foi adicionado à lista de compras.")

def excluir_item():
    nome = input("Digite o nome do item que deseja excluir: ")
    for item in lista_de_compras:
        if item["nome"] == nome:
            lista_de_compras.remove(item)
            if item["quantidade"] > 1:
                print(f"{item['quantidade']} unidades de {nome} foram removidas da lista de compras.")
            else:
                print(f"{nome} foi removido da lista de compras.")
            return
    print(f"{nome} não foi encontrado na lista de compras.")

def somar_preco():
    total = 0
    for item in lista_de_compras:
        total += item["preco"] * item["quantidade"]
    print(f"O preço total da lista de compras é R${total:.2f}")

def mostrar_lista():
    if len(lista_de_compras) == 0:
        print("A lista de compras está vazia.")
        return
    for item in lista_de_compras:
        nome = item['nome']
        preco = item['preco']
        quantidade = item['quantidade']
        total = preco * quantidade
        if quantidade > 1:
            print(f"{nome} (x{quantidade}) - R${total:.2f}")
        else:
            print(f"{nome} - R${total:.2f}")

def ordenar_por_nome():
    lista_de_compras.sort(key=lambda x: x["nome"])
    print("Lista de compras ordenada por nome:")

def ordenar_por_preco():
    for item in lista_de_compras:
        item["valor_total"] = item["preco"] * item["quantidade"]
    lista_de_compras.sort(key=lambda x: x["valor_total"], reverse=True)
    print("Lista de compras ordenada por preço:")

def ordenar_por_quantidade():
    lista_de_compras.sort(key=lambda x: x["quantidade"])
    print("Lista de compras ordenada por quantidade:")

while True:
    print("\n=== LISTA DE COMPRAS ===")
    print("1. Adicionar item")
    print("2. Excluir item")
    print("3. Mostrar lista de compras")
    print("4. Ordenar por nome")
    print("5. Ordenar por preço")
    print("6. Ordenar por quantidade")
    print("7. Somar preço")
    print("8. Sair")

    opcao = input("Digite uma opção (1-8): ")

    if opcao == "1":
        adicionar_item()
    elif opcao == "2":
        excluir_item()
    elif opcao == "3":
        mostrar_lista()
    elif opcao == "4":
        ordenar_por_nome()
        mostrar_lista()
    elif opcao == "5":
        ordenar_por_preco()
        mostrar_lista()
    elif opcao == "6":
        ordenar_por_quantidade()
        mostrar_lista()
    elif opcao == "7":
        somar_preco()
    elif opcao == "8":
        print("\n=== LISTA DE COMPRAS ===")
        mostrar_lista()
        print("\n========================")
        somar_preco()
        print("\n========================")
        break
    else:
        print("Insira uma opção válida!")
