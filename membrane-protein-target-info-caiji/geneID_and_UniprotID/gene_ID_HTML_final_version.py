from Bio import Entrez #从biopython导入Entrez包

Entrez.email = "xxxx@gmail.com" #这里填写你注册NCBI的邮箱，必须写，不然会被NCBI拒绝访问
#gene_list.txt，每一行是1个gene symbol，需要保存在与本python文件相同目录下
with open('gene_list.txt', 'r') as f:
    gene_list = [line.strip() for line in f]

#输入需要去检索gene ID的物种
species_list = ["Human", "Mouse", "Rat", "Monkey"]

#monkey可能有不止1个，只获取第1个monkey的gene ID，不能保证每个gene获取同一个monkey的gene ID
gene_dict = {}
for gene in gene_list:
    for species in species_list:
        if species == "Monkey":
            search_term = gene + "[gene] AND Primates[Organism]"
        else:
            search_term = gene + "[gene] AND " + species + "[Organism]"

        handle = Entrez.esearch(db="gene", term=search_term)
        record = Entrez.read(handle)
        id_list = record["IdList"]

        if len(id_list) > 0:
            gene_id = id_list[0]
            gene_dict[gene + "-" + species] = gene_id
        else:
            gene_dict[gene + "-" + species] = "NA"

link = "https://www.ncbi.nlm.nih.gov/gene/{}"

#将获取到的gene ID信息，转成HTML格式，并保存在名为“output.tsv“的文件中
with open('output.tsv', 'w') as outfile:
    outfile.write("Gene Name\tSpecies\tGene Link\tGene ID\n")
    for gene_species, gene_id in gene_dict.items():
        species_name = gene_species.split("-")[1]
        gene_name = gene_species.split("-")[0]
        #如果该物种的gene ID信息不存在，则为NA
        if gene_id != "NA":
            gene_link = link.format(gene_id)
            outfile.write("{}\t{}:\t<a href='{}'>{}</a>\t{}\n".format(gene_name, species_name, gene_link, gene_id, gene_id))
        else:
            outfile.write("{}\t{}:\t{}\t{}\n".format(gene_name, species_name, gene_id, gene_id))
