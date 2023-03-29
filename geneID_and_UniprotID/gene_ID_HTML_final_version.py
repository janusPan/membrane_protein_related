from Bio import Entrez

Entrez.email = "panyang19950603@gmail.com"
with open('gene_list.txt', 'r') as f:
    gene_list = [line.strip() for line in f]
species_list = ["Human", "Mouse", "Rat", "Monkey"]

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
with open('output.tsv', 'w') as outfile:
    outfile.write("Gene Name\tSpecies\tGene Link\tGene ID\n")
    for gene_species, gene_id in gene_dict.items():
        species_name = gene_species.split("-")[1]
        gene_name = gene_species.split("-")[0]
        if gene_id != "NA":
            gene_link = link.format(gene_id)
            outfile.write("{}\t{}:\t<a href='{}'>{}</a>\t{}\n".format(gene_name, species_name, gene_link, gene_id, gene_id))
        else:
            outfile.write("{}\t{}:\t{}\t{}\n".format(gene_name, species_name, gene_id, gene_id))
