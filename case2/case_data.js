/**
 * case_data.js — Ivy Tech IT Challenge 2026, Case 2
 * BIOL 101 course materials with assigned-instructor flag,
 * a question bank keyed by material ID, and a sample staff directory.
 *
 * Rules:
 *  - assigned_by_instructor: true  → appears in the default study view
 *  - assigned_by_instructor: false → available in full catalogue only
 *  - type: "reading" | "lecture_notes"  (both accepted by the same selector)
 */

const COURSE = {
  id: "BIOL101",
  title: "Introduction to Biology",
  section: "Fall 2026 — Section 004",
  instructor: "Prof. M. Torres"
};

const MATERIALS = [
  {
    id: "M01",
    type: "reading",
    title: "The Scientific Method",
    assigned_by_instructor: true,
    source_text: `The scientific method is a systematic process for investigating phenomena and acquiring new knowledge. It begins with observation, which leads to a question. A hypothesis—a testable, falsifiable explanation—is then proposed. Controlled experiments isolate a single variable (the independent variable) while holding all other conditions constant. Results are recorded as data, analyzed for patterns, and used to support or refute the hypothesis. If repeated experiments consistently support a hypothesis it may be elevated to a theory: a well-substantiated explanation. A scientific theory is not a guess; it is the highest level of scientific understanding. Peer review and replication are essential steps that protect against bias and error.`,
    excerpt: "The scientific method is a systematic process for investigating phenomena and acquiring new knowledge. It begins with observation, which leads to a question."
  },
  {
    id: "M02",
    type: "reading",
    title: "Cell Structure and Function",
    assigned_by_instructor: true,
    source_text: `All living organisms are composed of cells, the basic unit of life. Prokaryotic cells (bacteria and archaea) lack a membrane-bound nucleus; their DNA floats freely in the cytoplasm. Eukaryotic cells—found in plants, animals, fungi, and protists—contain a nucleus that houses the genetic material. Key organelles include the mitochondria (site of ATP production via cellular respiration), the endoplasmic reticulum (protein and lipid synthesis), the Golgi apparatus (processing and packaging proteins), and ribosomes (translating mRNA into protein). Plant cells additionally contain chloroplasts (photosynthesis) and a rigid cell wall composed of cellulose. The plasma membrane, a phospholipid bilayer, regulates what enters and exits every cell through selective permeability.`,
    excerpt: "All living organisms are composed of cells, the basic unit of life. Prokaryotic cells lack a membrane-bound nucleus; eukaryotic cells contain a nucleus."
  },
  {
    id: "M03",
    type: "lecture_notes",
    title: "Lecture Notes: Cell Division — Mitosis & Meiosis",
    assigned_by_instructor: true,
    source_text: `Cell division produces new cells from existing ones. Mitosis produces two genetically identical daughter cells and is used for growth, repair, and asexual reproduction. It proceeds through four stages: Prophase (chromosomes condense, spindle forms), Metaphase (chromosomes align at the cell's equator), Anaphase (sister chromatids separate toward opposite poles), and Telophase (nuclear envelopes reform, cytoplasm divides in cytokinesis). Meiosis produces four genetically unique haploid cells for sexual reproduction. It consists of two rounds of division (Meiosis I and II). During Meiosis I, homologous chromosomes separate; crossing over in prophase I increases genetic diversity. The result is gametes (sperm or egg) each carrying half the original chromosome number.`,
    excerpt: "Mitosis produces two genetically identical daughter cells. Meiosis produces four genetically unique haploid cells for sexual reproduction."
  },
  {
    id: "M04",
    type: "reading",
    title: "Photosynthesis and Cellular Respiration",
    assigned_by_instructor: true,
    source_text: `Photosynthesis converts light energy into chemical energy stored as glucose. It occurs in two stages in the chloroplast: the light-dependent reactions (in the thylakoid membrane) capture energy from sunlight to produce ATP, NADPH, and O₂; the Calvin cycle (in the stroma) uses that ATP and NADPH to fix CO₂ into glucose. The overall equation is: 6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂. Cellular respiration is essentially the reverse: glucose is oxidized to release ATP. Glycolysis occurs in the cytoplasm, the Krebs cycle in the mitochondrial matrix, and oxidative phosphorylation along the inner mitochondrial membrane. Each glucose molecule can yield up to 36–38 ATP molecules.`,
    excerpt: "Photosynthesis converts light energy into chemical energy stored as glucose. Cellular respiration releases that energy as ATP."
  },
  {
    id: "M05",
    type: "lecture_notes",
    title: "Lecture Notes: DNA Structure and Replication",
    assigned_by_instructor: true,
    source_text: `DNA (deoxyribonucleic acid) is a double helix composed of two antiparallel strands. Each strand is a polymer of nucleotides; each nucleotide contains a deoxyribose sugar, a phosphate group, and one of four nitrogenous bases: adenine (A), thymine (T), guanine (G), and cytosine (C). Base pairing is specific: A pairs with T (2 hydrogen bonds), G pairs with C (3 hydrogen bonds). During replication, helicase unwinds the helix at the origin of replication, creating a replication fork. DNA polymerase synthesizes new strands in a 5'→3' direction using each original strand as a template. Because each new molecule contains one original and one new strand, replication is semiconservative. Proofreading by DNA polymerase reduces errors to roughly 1 per billion base pairs.`,
    excerpt: "DNA is a double helix. During replication, DNA polymerase synthesizes new strands using each original strand as a template (semiconservative)."
  },
  // --- NOT assigned by instructor (catalogue only) ---
  {
    id: "M06",
    type: "reading",
    title: "Ecology: Populations and Communities",
    assigned_by_instructor: false,
    source_text: `A population is a group of individuals of the same species living in the same area. Population dynamics are governed by birth rate, death rate, immigration, and emigration. Carrying capacity (K) is the maximum population size an environment can sustain. Communities consist of multiple interacting populations. Key interactions include predation, competition, mutualism, commensalism, and parasitism. Ecological succession describes how communities change over time, from pioneer species (e.g., lichens on bare rock) to a stable climax community.`,
    excerpt: "A population is a group of individuals of the same species. Carrying capacity is the maximum population size an environment can sustain."
  },
  {
    id: "M07",
    type: "reading",
    title: "Evolution and Natural Selection",
    assigned_by_instructor: false,
    source_text: `Evolution is a change in the heritable characteristics of populations over successive generations. Natural selection, described by Charles Darwin, is the primary mechanism: individuals with traits better suited to their environment survive and reproduce more successfully. For natural selection to act there must be variation, heritability, and differential reproductive success. Other mechanisms include genetic drift, gene flow, and mutation. Speciation—the formation of new species—can occur through allopatric (geographic isolation) or sympatric (non-geographic) processes.`,
    excerpt: "Evolution is a change in heritable characteristics over generations. Natural selection acts on variation to increase reproductive success."
  },
  {
    id: "M08",
    type: "lecture_notes",
    title: "Lecture Notes: Genetics — Mendelian Inheritance",
    assigned_by_instructor: false,
    source_text: `Gregor Mendel's experiments with pea plants established the foundational rules of inheritance. The Law of Segregation states that allele pairs separate during gamete formation so each gamete carries one allele per gene. The Law of Independent Assortment states that genes on different chromosomes are distributed independently. Dominant alleles mask recessive alleles; heterozygous individuals show the dominant phenotype. Punnett squares predict the probability of offspring genotypes. Incomplete dominance, codominance, and sex-linked traits extend beyond simple Mendelian ratios.`,
    excerpt: "Mendel's Law of Segregation: allele pairs separate during gamete formation. Law of Independent Assortment: genes on different chromosomes distribute independently."
  },
  {
    id: "M09",
    type: "reading",
    title: "The Immune System",
    assigned_by_instructor: false,
    source_text: `The immune system protects the body against pathogens. Innate immunity provides non-specific, immediate defenses including physical barriers (skin, mucous membranes) and phagocytic cells (neutrophils, macrophages). Adaptive immunity is specific and develops memory. B cells produce antibodies (humoral immunity); T cells destroy infected cells or regulate immune responses (cell-mediated immunity). The two-signal model of T cell activation prevents autoimmunity. Vaccines exploit immunological memory to protect against future infection.`,
    excerpt: "Innate immunity provides non-specific defenses. Adaptive immunity is specific: B cells produce antibodies, T cells destroy infected cells."
  },
  {
    id: "M10",
    type: "lecture_notes",
    title: "Lecture Notes: Biotechnology and Genomics",
    assigned_by_instructor: false,
    source_text: `Biotechnology applies biological systems to develop products and processes. Key techniques include PCR (polymerase chain reaction) to amplify DNA, gel electrophoresis to separate DNA fragments by size, recombinant DNA technology to insert genes into host organisms, and CRISPR-Cas9 for precise gene editing. Genomics is the large-scale study of all genes in an organism. The Human Genome Project (completed 2003) sequenced all ~3 billion base pairs of human DNA. Bioinformatics uses computational tools to store, retrieve, and analyze sequence data.`,
    excerpt: "PCR amplifies DNA. CRISPR-Cas9 enables precise gene editing. The Human Genome Project sequenced all ~3 billion base pairs of human DNA."
  }
];

/**
 * Question bank — keyed by material ID.
 * Each entry: { question, options: [A,B,C,D], answer: "A"|"B"|"C"|"D", explanation, source_excerpt }
 */
const QUESTION_BANK = {
  M01: [
    {
      question: "What distinguishes a scientific theory from a hypothesis?",
      options: [
        "A theory is a guess; a hypothesis has been tested.",
        "A theory is well-substantiated by repeated experimentation; a hypothesis is an initial testable explanation.",
        "A theory cannot be revised; a hypothesis can be.",
        "A theory is based on opinion; a hypothesis is based on data."
      ],
      answer: "B",
      explanation: "A hypothesis is a testable explanation proposed before experimentation. A theory is the highest level of scientific understanding, supported by repeated, peer-reviewed experiments.",
      source_excerpt: "If repeated experiments consistently support a hypothesis it may be elevated to a theory: a well-substantiated explanation."
    }
  ],
  M02: [
    {
      question: "Which organelle is primarily responsible for producing ATP through cellular respiration?",
      options: [
        "Ribosome",
        "Golgi apparatus",
        "Mitochondria",
        "Endoplasmic reticulum"
      ],
      answer: "C",
      explanation: "Mitochondria carry out cellular respiration, converting glucose and oxygen into ATP, the cell's primary energy currency.",
      source_excerpt: "Key organelles include the mitochondria (site of ATP production via cellular respiration)."
    },
    {
      question: "What structural feature do plant cells have that animal cells lack?",
      options: [
        "Plasma membrane",
        "Mitochondria",
        "Ribosomes",
        "Cell wall composed of cellulose"
      ],
      answer: "D",
      explanation: "Plant cells have a rigid cell wall made of cellulose that provides structural support, which animal cells do not have.",
      source_excerpt: "Plant cells additionally contain chloroplasts (photosynthesis) and a rigid cell wall composed of cellulose."
    }
  ],
  M03: [
    {
      question: "During which phase of mitosis do chromosomes align at the cell's equator?",
      options: [
        "Prophase",
        "Metaphase",
        "Anaphase",
        "Telophase"
      ],
      answer: "B",
      explanation: "During Metaphase, the spindle fibers pull chromosomes to the middle of the cell (the metaphase plate) before they are separated.",
      source_excerpt: "Metaphase (chromosomes align at the cell's equator)."
    },
    {
      question: "What is the main function of crossing over during Meiosis I?",
      options: [
        "To replicate DNA before division",
        "To increase genetic diversity among gametes",
        "To separate sister chromatids",
        "To produce ATP for cell division"
      ],
      answer: "B",
      explanation: "Crossing over exchanges segments between homologous chromosomes, shuffling alleles and creating genetically unique gametes.",
      source_excerpt: "crossing over in prophase I increases genetic diversity."
    }
  ],
  M04: [
    {
      question: "Where does the Calvin cycle (light-independent reactions) take place?",
      options: [
        "Thylakoid membrane",
        "Cytoplasm",
        "Mitochondrial matrix",
        "Stroma of the chloroplast"
      ],
      answer: "D",
      explanation: "The Calvin cycle occurs in the stroma of the chloroplast, using ATP and NADPH from the light reactions to fix CO₂ into glucose.",
      source_excerpt: "the Calvin cycle (in the stroma) uses that ATP and NADPH to fix CO₂ into glucose."
    }
  ],
  M05: [
    {
      question: "Why is DNA replication described as 'semiconservative'?",
      options: [
        "Half of the DNA is destroyed and rebuilt each cycle.",
        "Each new DNA molecule contains one original strand and one newly synthesized strand.",
        "Only the coding strand is copied.",
        "Replication conserves exactly half the original base pairs."
      ],
      answer: "B",
      explanation: "Semiconservative replication means each daughter molecule keeps one parental strand as a template, ensuring accurate copying.",
      source_excerpt: "Because each new molecule contains one original and one new strand, replication is semiconservative."
    }
  ],
  M06: [
    {
      question: "What is carrying capacity in ecology?",
      options: [
        "The number of species in a community",
        "The maximum population size an environment can sustain",
        "The rate of immigration into a population",
        "The minimum viable population size"
      ],
      answer: "B",
      explanation: "Carrying capacity (K) is the maximum number of individuals an environment can support given its limited resources.",
      source_excerpt: "Carrying capacity (K) is the maximum population size an environment can sustain."
    }
  ],
  M07: [
    {
      question: "Which of the following is NOT required for natural selection to occur?",
      options: [
        "Variation among individuals",
        "Heritability of traits",
        "Geographic isolation",
        "Differential reproductive success"
      ],
      answer: "C",
      explanation: "Geographic isolation drives allopatric speciation but is not a prerequisite for natural selection, which requires only variation, heritability, and differential reproduction.",
      source_excerpt: "For natural selection to act there must be variation, heritability, and differential reproductive success."
    }
  ],
  M08: [
    {
      question: "What does Mendel's Law of Segregation state?",
      options: [
        "Genes on different chromosomes are distributed independently.",
        "Allele pairs separate during gamete formation so each gamete carries one allele.",
        "Dominant alleles always mask recessive alleles.",
        "Offspring inherit traits from only one parent."
      ],
      answer: "B",
      explanation: "The Law of Segregation states that the two alleles for each gene segregate during meiosis so each gamete receives only one.",
      source_excerpt: "The Law of Segregation states that allele pairs separate during gamete formation so each gamete carries one allele per gene."
    }
  ],
  M09: [
    {
      question: "Which cells are responsible for producing antibodies in adaptive immunity?",
      options: [
        "Neutrophils",
        "Macrophages",
        "T cells",
        "B cells"
      ],
      answer: "D",
      explanation: "B cells differentiate into plasma cells that secrete antibodies targeting specific antigens in the humoral immune response.",
      source_excerpt: "B cells produce antibodies (humoral immunity)."
    }
  ],
  M10: [
    {
      question: "What is the primary purpose of PCR (polymerase chain reaction)?",
      options: [
        "To separate DNA fragments by size",
        "To insert genes into host organisms",
        "To amplify a specific DNA sequence",
        "To edit genes with precision"
      ],
      answer: "C",
      explanation: "PCR uses repeated cycles of heating and cooling with a thermostable polymerase to amplify a specific DNA segment from a tiny sample.",
      source_excerpt: "PCR (polymerase chain reaction) to amplify DNA."
    }
  ]
};

/** Sample staff directory for the human-help link */
const HELP_DIRECTORY = [
  {
    name: "Academic Support Center",
    role: "Tutoring & Study Help",
    contact: "academic-support@ivytech.edu",
    hours: "Mon–Thu 8am–8pm · Fri 8am–5pm",
    phone: "(317) 921-4800"
  },
  {
    name: "Prof. M. Torres",
    role: "BIOL 101 Instructor",
    contact: "mtorres@ivytech.edu",
    hours: "Office hours: Tue/Thu 2–4pm",
    phone: null
  },
  {
    name: "Ivy Tech Online Help Desk",
    role: "Technical & Course Access Issues",
    contact: "helpdesk@ivytech.edu",
    hours: "24/7 phone & chat",
    phone: "1-888-IVY-LINE"
  }
];

export { COURSE, MATERIALS, QUESTION_BANK, HELP_DIRECTORY };
