
# VSCode does not add the root directory to the path (by default?). Not sure why
# this works sometimes and not others. This is a workaround.
import sys

# sys.path.insert(0, "../og_biocypher/biocypher")
sys.path.insert(0, "")
from biocypher import BioCypher

from otar_biocypher.target_disease_evidence_adapter import (
    TargetDiseaseEvidenceAdapter,
    TargetDiseaseDataset,
    TargetNodeField,
    DiseaseNodeField,
    DrugNodeField,
    DrugGeneEdgeField,
    TargetDiseaseEdgeField,
    GeneOntologyNodeField,
    MousePhenotypeNodeField,
    MouseTargetNodeField,
    TargetGoEdgeField,
    MouseModelNodeField,
    DrugDiseaseEdgeField,
    MouseModelToTarget
)

"""
Configuration: select datasets and fields to be imported.

`datasets`: list of datasets to be imported. See 
target_disease_evidence_adapter.py for available datasets or use
`TargetDiseaseDataset` Enum auto-complete.

`node_field`: list of fields to be imported for each of the types of nodes that
the adapter creates. See target_disease_evidence_adapter.py for available fields
or use Enum auto-complete of `TargetNodeField`, `DiseaseNodeField`,
`GeneOntologyNodeField`, `MousePhenotypeNodeField`, `MouseTargetNodeField`. Note
that some fields are mandatory for the functioning of the adapter (primary
identifiers) and some are optional (e.g. gene symbol).

`edge_fields`: list of fields to be imported for each of the relationships that
the adapter creates. See target_disease_evidence_adapter.py for available fields
or use Enum auto-complete of `TargetDiseaseEdgeField`. Note that some fields are
mandatory for the functioning of the adapter (primary identifiers) and some are
optional (e.g.  score).
"""

target_disease_datasets = [
    TargetDiseaseDataset.CANCER_BIOMARKERS,
    TargetDiseaseDataset.CANCER_GENE_CENSUS,
    TargetDiseaseDataset.CHEMBL,
    TargetDiseaseDataset.CLINGEN,
    TargetDiseaseDataset.CRISPR,
    TargetDiseaseDataset.EUROPE_PMC,
    TargetDiseaseDataset.EVA,
    TargetDiseaseDataset.EVA_SOMATIC,
    TargetDiseaseDataset.EXPRESSION_ATLAS,
    TargetDiseaseDataset.GENOMICS_ENGLAND,
    TargetDiseaseDataset.GENE_BURDEN,
    TargetDiseaseDataset.GENE2PHENOTYPE,
    TargetDiseaseDataset.IMPC,
    TargetDiseaseDataset.INTOGEN,
    TargetDiseaseDataset.ORPHANET,
    TargetDiseaseDataset.OT_GENETICS_PORTAL,
    TargetDiseaseDataset.PROGENY,
    TargetDiseaseDataset.REACTOME,
    TargetDiseaseDataset.SLAP_ENRICH,
    TargetDiseaseDataset.SYSBIO,
    TargetDiseaseDataset.UNIPROT_VARIANTS,
    TargetDiseaseDataset.UNIPROT_LITERATURE,
]

target_disease_node_fields = [
    # mandatory fields
    TargetNodeField.TARGET_GENE_ENSG,
    DiseaseNodeField.DISEASE_ACCESSION,
    GeneOntologyNodeField.GENE_ONTOLOGY_ACCESSION,
    MousePhenotypeNodeField.MOUSE_PHENOTYPE_ACCESSION,
    MouseTargetNodeField.MOUSE_TARGET_ENSG,
    DrugNodeField.MOLECULE_ID,

    # optional target (gene) fields
    TargetNodeField.TARGET_GENE_SYMBOL,
    TargetNodeField.TARGET_GENE_BIOTYPE,
    # optional disease fields
    DiseaseNodeField.DISEASE_CODE,
    DiseaseNodeField.DISEASE_NAME,
    DiseaseNodeField.DISEASE_DESCRIPTION,
    # optional gene ontology fields
    GeneOntologyNodeField.GENE_ONTOLOGY_NAME,
    # optional mouse phenotype fields
    MousePhenotypeNodeField.MOUSE_PHENOTYPE_LABEL,
    # optional mouse target fields
    MouseTargetNodeField.MOUSE_TARGET_ENSG,
    MouseTargetNodeField.MOUSE_TARGET_SYMBOL,
    MouseTargetNodeField.MOUSE_TARGET_MGI,

    MouseModelNodeField.MOUSE_PHENOTYPE_MODELS, 
    MouseModelNodeField.MOUSE_PHENOTYPE_CLASSES_ID, 
    MouseModelNodeField.MOUSE_PHENOTYPE_CLASSES_LABEL, 

    DrugNodeField.DRUGTYPE,
    DrugNodeField.INCHIKEY,
    DrugNodeField.NAME,
    DrugNodeField.ISAPPROVED,
    DrugNodeField.DESCRIPTION,
]

target_disease_edge_fields = [
    # mandatory fields
    TargetDiseaseEdgeField.INTERACTION_ACCESSION,
    TargetDiseaseEdgeField.TARGET_GENE_ENSG,
    TargetDiseaseEdgeField.DISEASE_ACCESSION,
    TargetDiseaseEdgeField.ASSOCIATION_TYPE,
    TargetDiseaseEdgeField.SOURCE,
    # optional fields
    TargetDiseaseEdgeField.SCORE,
    TargetDiseaseEdgeField.LITERATURE,
    TargetGoEdgeField.TARGET_GENE_ENSG,
    TargetGoEdgeField.GO_ACCESSION,
    TargetGoEdgeField.TYPE,
    TargetGoEdgeField.SOURCE,
    TargetGoEdgeField.LITERATURE,
    TargetGoEdgeField.GENEPRODUCT,
    TargetGoEdgeField.ECOID,
    DrugGeneEdgeField.DRUG_ID,
    DrugGeneEdgeField.GENE_ID,
    DrugDiseaseEdgeField.DRUG_ID,
    DrugDiseaseEdgeField.DISEASE_ID,
    MouseModelToTarget.MOUSE_MODEL_ID,
    MouseModelToTarget.TARGET_HUMAN_GENE,
    MouseModelToTarget.SOURCE
]


def main():
    """
    Main function running the import using BioCypher and the adapter.
    """

    # Start BioCypher
    bc = BioCypher(
        biocypher_config_path="config/biocypher_config.yaml",
    )

    # Check the schema
    bc.show_ontology_structure()

    # Load data

    # Open Targets
    target_disease_adapter = TargetDiseaseEvidenceAdapter(
        datasets=target_disease_datasets,
        node_fields=target_disease_node_fields,
        edge_fields=target_disease_edge_fields,
        test_mode=True,
        test_mode_size = [100000,30000]
    )

    target_disease_adapter.load_data(
        stats=False,
        show_nodes=False,
        show_edges=False,
    )

    # Write nodes
    bc.write_nodes(target_disease_adapter.get_nodes())

    # Write OTAR edges in batches to avoid memory issues
    target_disease_adapter.get_edge_batches()
    bc.write_edges(target_disease_adapter.get_edges())

    # Post import functions
    bc.write_import_call()
    bc.summary()


if __name__ == "__main__":
    main()
