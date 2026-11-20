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
/**
 * HELP_OPTIONS — runtime equivalent of help_options.csv.
 * Schema: { id, name, role, best_for, availability, contact_type,
 *           contact_value, directions, is_24_7, sample_data: true }
 * contact_type: "email" | "phone" | "portal" | "chat"
 * For portal routes with no live URL, directions explains how to reach them.
 */
const HELP_OPTIONS = [
  {
    id: "online-tutoring",
    name: "Online Tutoring (24/7)",
    role: "Late-night content help",
    best_for: "Content questions about readings and lecture notes, any time of day or night",
    availability: "24 hours a day, 7 days a week",
    contact_type: "portal",
    contact_value: null,
    directions: "Log in to MyIvy → Student Services → Tutoring → Start a Session. Choose Biology from the subject list.",
    is_24_7: true,
    sample_data: true
  },
  {
    id: "biology-tutor",
    name: "Biology Tutoring Center",
    role: "Scheduled biology tutoring",
    best_for: "In-depth help with BIOL 101 concepts, lab prep, and exam review",
    availability: "Mon/Wed 10am–2pm · Tue/Thu 1pm–5pm · Sat 10am–1pm",
    contact_type: "email",
    contact_value: "bio-tutoring@ivytech.edu",
    directions: null,
    is_24_7: false,
    sample_data: true
  },
  {
    id: "instructor",
    name: "Prof. M. Torres",
    role: "BIOL 101 Instructor",
    best_for: "Questions about graded work, assignment requirements, or course policies",
    availability: "Office hours: Tue/Thu 2–4pm · or by appointment",
    contact_type: "email",
    contact_value: "mtorres@ivytech.edu",
    directions: null,
    is_24_7: false,
    sample_data: true
  },
  {
    id: "help-desk",
    name: "Ivy Tech Help Desk",
    role: "Technical & account issues",
    best_for: "Login problems, Blackboard access, or anything technical",
    availability: "24/7 phone & chat",
    contact_type: "phone",
    contact_value: "1-888-IVY-LINE",
    directions: null,
    is_24_7: true,
    sample_data: false
  }
];

/** @deprecated — kept for backwards compatibility; use HELP_OPTIONS instead */
const HELP_DIRECTORY = HELP_OPTIONS.map(h => ({
  name: h.name,
  role: h.role,
  contact: h.contact_value || h.directions || "",
  hours: h.availability,
  phone: h.contact_type === "phone" ? h.contact_value : null
}));

/**
 * KEY_TERMS — keyed by material ID.
 * Sourced from material source_text (invented examples; will be replaced by
 * data/key_terms.csv when that file is provided on challenge day).
 * Each entry: { term: string, definition: string }
 *
 * NOTE: data/key_terms.csv schema (when available):
 *   material_id, term, definition
 * Loader pattern matches app/lib/data.py's read_any() — drop CSV in data/
 * and update this object (or fetch it at runtime).
 */
const KEY_TERMS = {
  M01: [
    { term: "Hypothesis",        definition: "A testable, falsifiable explanation for an observation, proposed before experimentation." },
    { term: "Independent variable", definition: "The single factor deliberately changed in a controlled experiment." },
    { term: "Scientific theory",  definition: "A well-substantiated explanation supported by repeated, peer-reviewed experiments — the highest level of scientific understanding." },
    { term: "Peer review",        definition: "Evaluation of scientific work by other experts before publication, protecting against bias and error." }
  ],
  M02: [
    { term: "Prokaryotic cell",   definition: "A cell without a membrane-bound nucleus; DNA floats freely in the cytoplasm. Bacteria and archaea are prokaryotes." },
    { term: "Eukaryotic cell",    definition: "A cell with a membrane-bound nucleus housing its genetic material. Found in plants, animals, fungi, and protists." },
    { term: "Mitochondria",       definition: "Organelle that produces ATP via cellular respiration; often called the 'powerhouse of the cell'." },
    { term: "Phospholipid bilayer", definition: "The two-layered structure of the plasma membrane that controls what enters and exits a cell (selective permeability)." },
    { term: "Golgi apparatus",    definition: "Organelle that processes and packages proteins for secretion or use within the cell." }
  ],
  M03: [
    { term: "Mitosis",            definition: "Cell division producing two genetically identical daughter cells; used for growth and repair." },
    { term: "Meiosis",            definition: "Cell division producing four genetically unique haploid cells; used for sexual reproduction." },
    { term: "Prophase",           definition: "First stage of mitosis: chromosomes condense and the spindle begins to form." },
    { term: "Metaphase",          definition: "Stage of mitosis where chromosomes align at the cell's equatorial plate." },
    { term: "Crossing over",      definition: "Exchange of chromosome segments between homologous chromosomes during Meiosis I, increasing genetic diversity." },
    { term: "Cytokinesis",        definition: "Division of the cytoplasm following nuclear division, completing cell separation." }
  ],
  M04: [
    { term: "Photosynthesis",     definition: "The process by which chloroplasts convert light energy into chemical energy (glucose). Equation: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂." },
    { term: "Calvin cycle",       definition: "The light-independent reactions in the stroma of the chloroplast that use ATP and NADPH to fix CO₂ into glucose." },
    { term: "Cellular respiration", definition: "The process of oxidizing glucose to release ATP; occurs via glycolysis, the Krebs cycle, and oxidative phosphorylation." },
    { term: "ATP",                definition: "Adenosine triphosphate — the primary energy currency of cells, produced by mitochondria." },
    { term: "Thylakoid membrane", definition: "The membrane inside a chloroplast where the light-dependent reactions of photosynthesis occur." }
  ],
  M05: [
    { term: "DNA",                definition: "Deoxyribonucleic acid — a double helix polymer of nucleotides that carries genetic information." },
    { term: "Nucleotide",         definition: "The monomer of DNA, consisting of a deoxyribose sugar, a phosphate group, and one of four nitrogenous bases (A, T, G, or C)." },
    { term: "Base pairing",       definition: "Specific hydrogen-bond pairing: adenine (A) with thymine (T), guanine (G) with cytosine (C)." },
    { term: "Semiconservative replication", definition: "Each new DNA molecule contains one original strand and one newly synthesized strand." },
    { term: "DNA polymerase",     definition: "Enzyme that synthesizes new DNA strands in the 5'→3' direction and proofreads for errors." },
    { term: "Helicase",           definition: "Enzyme that unwinds the DNA double helix at the replication fork during DNA replication." }
  ],
  M06: [
    { term: "Population",         definition: "A group of individuals of the same species living in the same area." },
    { term: "Carrying capacity",  definition: "The maximum population size an environment can sustain given its resources (symbolized K)." },
    { term: "Ecological succession", definition: "Gradual change in a community over time, from pioneer species to a stable climax community." }
  ],
  M07: [
    { term: "Natural selection",  definition: "The mechanism of evolution: individuals with advantageous traits survive and reproduce more, passing those traits on." },
    { term: "Genetic drift",      definition: "Random changes in allele frequencies in a population, more pronounced in small populations." },
    { term: "Speciation",         definition: "The formation of new species; can occur through geographic isolation (allopatric) or without it (sympatric)." }
  ],
  M08: [
    { term: "Law of Segregation", definition: "Mendel's first law: allele pairs separate during gamete formation so each gamete carries one allele per gene." },
    { term: "Law of Independent Assortment", definition: "Mendel's second law: genes on different chromosomes distribute independently during gamete formation." },
    { term: "Dominant allele",    definition: "An allele whose phenotype is expressed even when only one copy is present (masks the recessive allele)." },
    { term: "Punnett square",     definition: "A grid used to predict the probability of offspring genotypes from a genetic cross." }
  ],
  M09: [
    { term: "Innate immunity",    definition: "Non-specific, immediate defense mechanisms including physical barriers and phagocytic cells." },
    { term: "Adaptive immunity",  definition: "Specific immune response that develops immunological memory; involves B cells and T cells." },
    { term: "Antibody",           definition: "A protein produced by B cells that binds to a specific antigen to neutralize or mark it for destruction." },
    { term: "Vaccine",            definition: "A preparation that trains the immune system to recognize a pathogen, exploiting immunological memory." }
  ],
  M10: [
    { term: "PCR",                definition: "Polymerase chain reaction — a technique to amplify a specific DNA sequence using repeated heating and cooling cycles." },
    { term: "CRISPR-Cas9",        definition: "A precise gene-editing tool that uses a guide RNA to direct the Cas9 protein to cut a specific DNA sequence." },
    { term: "Gel electrophoresis", definition: "A technique that separates DNA fragments by size using an electric field and a gel matrix." },
    { term: "Genomics",           definition: "The large-scale study of all genes in an organism, including their functions and interactions." }
  ]
};

/**
 * KEY_TERMS_ES — Spanish glossary, keyed by material ID.
 * Source: sample CSV rows (data/key_terms_es.csv — not yet on disk).
 * Only assigned materials M01–M05 have sample Spanish rows.
 * Label: "Traducción de muestra — no verificada / Sample translation — not verified"
 */
const KEY_TERMS_ES = {
  M01: [
    { term: "Hypothesis",        definition_es: "Una explicación comprobable y falsificable de una observación, propuesta antes de la experimentación." },
    { term: "Independent variable", definition_es: "El único factor que se cambia deliberadamente en un experimento controlado." },
    { term: "Scientific theory",  definition_es: "Una explicación bien fundamentada respaldada por experimentos repetidos y revisados por pares — el nivel más alto de comprensión científica." },
    { term: "Peer review",        definition_es: "Evaluación del trabajo científico por otros expertos antes de su publicación, para proteger contra sesgos y errores." }
  ],
  M02: [
    { term: "Prokaryotic cell",   definition_es: "Una célula sin núcleo delimitado por membrana; el ADN flota libremente en el citoplasma. Las bacterias y las arqueas son procariotas." },
    { term: "Eukaryotic cell",    definition_es: "Una célula con núcleo delimitado por membrana que alberga el material genético. Se encuentra en plantas, animales, hongos y protistas." },
    { term: "Mitochondria",       definition_es: "Orgánulo que produce ATP mediante la respiración celular; a menudo llamado la 'central eléctrica de la célula'." },
    { term: "Phospholipid bilayer", definition_es: "La estructura de dos capas de la membrana plasmática que controla lo que entra y sale de una célula (permeabilidad selectiva)." },
    { term: "Golgi apparatus",    definition_es: "Orgánulo que procesa y empaqueta proteínas para su secreción o uso dentro de la célula." }
  ],
  M03: [
    { term: "Mitosis",            definition_es: "División celular que produce dos células hijas genéticamente idénticas; utilizada para el crecimiento y la reparación." },
    { term: "Meiosis",            definition_es: "División celular que produce cuatro células haploides genéticamente únicas; utilizada para la reproducción sexual." },
    { term: "Prophase",           definition_es: "Primera etapa de la mitosis: los cromosomas se condensan y comienza a formarse el huso acromático." },
    { term: "Metaphase",          definition_es: "Etapa de la mitosis en la que los cromosomas se alinean en la placa ecuatorial de la célula." },
    { term: "Crossing over",      definition_es: "Intercambio de segmentos de cromosomas entre cromosomas homólogos durante la Meiosis I, aumentando la diversidad genética." },
    { term: "Cytokinesis",        definition_es: "División del citoplasma después de la división nuclear, completando la separación celular." }
  ],
  M04: [
    { term: "Photosynthesis",     definition_es: "El proceso por el cual los cloroplastos convierten la energía luminosa en energía química (glucosa). Ecuación: 6CO₂ + 6H₂O + luz → C₆H₁₂O₆ + 6O₂." },
    { term: "Calvin cycle",       definition_es: "Las reacciones independientes de la luz en el estroma del cloroplasto que usan ATP y NADPH para fijar CO₂ en glucosa." },
    { term: "Cellular respiration", definition_es: "El proceso de oxidar glucosa para liberar ATP; ocurre mediante la glucólisis, el ciclo de Krebs y la fosforilación oxidativa." },
    { term: "ATP",                definition_es: "Trifosfato de adenosina — la principal moneda energética de las células, producida por las mitocondrias." },
    { term: "Thylakoid membrane", definition_es: "La membrana dentro de un cloroplasto donde ocurren las reacciones dependientes de la luz de la fotosíntesis." }
  ],
  M05: [
    { term: "DNA",                definition_es: "Ácido desoxirribonucleico — un polímero de doble hélice de nucleótidos que porta la información genética." },
    { term: "Nucleotide",         definition_es: "El monómero del ADN, que consta de un azúcar desoxirribosa, un grupo fosfato y una de cuatro bases nitrogenadas (A, T, G o C)." },
    { term: "Base pairing",       definition_es: "Emparejamiento específico por puentes de hidrógeno: adenina (A) con timina (T), guanina (G) con citosina (C)." },
    { term: "Semiconservative replication", definition_es: "Cada nueva molécula de ADN contiene una cadena original y una cadena recién sintetizada." },
    { term: "DNA polymerase",     definition_es: "Enzima que sintetiza nuevas cadenas de ADN en dirección 5'→3' y corrige errores." },
    { term: "Helicase",           definition_es: "Enzima que desenrolla la doble hélice de ADN en la horquilla de replicación durante la replicación del ADN." }
  ]
};

/**
 * PLAIN_ENGLISH_BULLETS — deterministic plain-language summaries, keyed by
 * material ID. Only assigned materials M01–M05 included.
 * Rules: shorter sentences, key terms defined on first use, scientific names kept.
 */
const PLAIN_ENGLISH_BULLETS = {
  M01: [
    "Scientists follow a step-by-step process to answer questions. It starts with noticing something interesting (observation), then asking a question about it.",
    "A hypothesis is an educated guess you can test. You change one thing at a time (the independent variable) to see what happens, while keeping everything else the same.",
    "Data from experiments either support the hypothesis or show it needs changing. Science works by testing ideas over and over.",
    "A theory is not a guess — it is an explanation that has been tested many times by many scientists. It is the highest level of scientific understanding.",
    "Peer review means other scientists check the work before it gets published. This catches mistakes and keeps science trustworthy."
  ],
  M02: [
    "Every living thing is made of cells — the smallest unit of life. Bacteria cells (prokaryotes) have no nucleus. Plant and animal cells (eukaryotes) have a nucleus that holds DNA.",
    "Inside eukaryotic cells are organelles, each with a job. Mitochondria make energy (ATP) through cellular respiration — think of them as tiny power plants.",
    "The ribosome builds proteins. The endoplasmic reticulum moves proteins and lipids around. The Golgi apparatus packages them for delivery.",
    "Plant cells have two extras: chloroplasts (for photosynthesis) and a stiff cell wall made of cellulose that holds the cell's shape.",
    "Every cell is wrapped in a plasma membrane — a phospholipid bilayer that controls what gets in and out."
  ],
  M03: [
    "Cells divide to let the body grow, heal, and reproduce. There are two main types: mitosis (for growth) and meiosis (for reproduction).",
    "Mitosis makes two identical copies. It has four stages: Prophase (chromosomes appear), Metaphase (they line up), Anaphase (they split), Telophase (two nuclei form). Then the cell splits — called cytokinesis.",
    "Meiosis makes four cells with half the usual number of chromosomes — these become sperm or egg cells. It goes through two rounds of division.",
    "During Meiosis I, chromosomes swap segments in a process called crossing over. This mixes genetic information so offspring are not identical to their parents.",
    "Think of it this way: mitosis = copy machine (identical); meiosis = shuffling a deck of cards (new combinations every time)."
  ],
  M04: [
    "Photosynthesis is how plants make food from sunlight. Inside leaf cells, chloroplasts turn water and CO₂ into glucose (sugar) and oxygen.",
    "It has two stages: the light reactions (in the thylakoid membrane) capture sunlight as ATP and NADPH. The Calvin cycle (in the stroma) uses that energy to build glucose.",
    "Simple equation: 6 CO₂ + 6 H₂O + sunlight → glucose + 6 O₂. The plant uses the glucose; the oxygen is what we breathe.",
    "Cellular respiration reverses this: cells break glucose down to release ATP energy. It happens via glycolysis, the Krebs cycle, and oxidative phosphorylation in the mitochondria.",
    "One glucose molecule can produce up to 36–38 ATP molecules — a highly efficient energy process."
  ],
  M05: [
    "DNA (deoxyribonucleic acid) stores your genetic instructions in a twisted ladder shape called a double helix. The 'rungs' are base pairs: A always pairs with T, G always pairs with C.",
    "Before a cell divides, it copies all its DNA so each new cell gets a full set. This is called DNA replication.",
    "An enzyme called helicase unzips the two strands. Then DNA polymerase reads each strand and builds a new matching strand alongside it.",
    "Because each new molecule keeps one original strand and gains one new strand, the process is called semiconservative replication.",
    "DNA polymerase is very accurate — about one error per billion base pairs — because it proofreads its own work."
  ]
};

export { COURSE, MATERIALS, QUESTION_BANK, KEY_TERMS, KEY_TERMS_ES,
         PLAIN_ENGLISH_BULLETS, HELP_OPTIONS, HELP_DIRECTORY };
