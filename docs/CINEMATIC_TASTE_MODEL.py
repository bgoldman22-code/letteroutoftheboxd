"""
CINEMATIC TASTE COGNITIVE MODEL
═══════════════════════════════════════════════════════════════════

A comprehensive system for modeling the psychological, aesthetic, emotional,
cinematic, and philosophical dimensions of film taste.

This goes far beyond genre, plot, or rating — it models WHY people connect
with certain films at a deep cognitive and emotional level.

TOTAL DIMENSIONS: 58 measurable taste vectors
Each scored on 1-7 scale for vector embedding similarity
"""

CINEMATIC_TASTE_DIMENSIONS = {
    
    # ═══════════════════════════════════════════════════════════════
    # A. CINEMATOGRAPHY & VISUAL LANGUAGE (15 dimensions)
    # ═══════════════════════════════════════════════════════════════
    
    "visual_language": {
        
        "color_palette_psychology": {
            "scale": "1 (muted earth tones) → 7 (saturated neon intensity)",
            "what_it_measures": "Emotional temperature and psychological distance communicated through color",
            "why_it_matters": "Color is subconscious emotion. Some viewers need warmth, others need alienation",
            "examples": {
                "1-2": ["The Rider", "Nomadland", "The Assassination of Jesse James"],
                "description_low": "Muted, desaturated, earth tones - evokes melancholy, realism, earthbound emotion",
                "viewer_resonance_low": "Viewers who process emotion through quiet observation, who find beauty in restraint",
                "6-7": ["Spring Breakers", "Enter the Void", "Drive"],
                "description_high": "Neon, saturated, hyper-real - evokes fever dream, heightened reality, sensory assault",
                "viewer_resonance_high": "Viewers who want cinema as altered state, who crave intensity and visual ecstasy"
            }
        },
        
        "lighting_philosophy": {
            "scale": "1 (naturalistic available light) → 7 (expressionistic chiaroscuro)",
            "what_it_measures": "How light is used to reveal or conceal psychological truth",
            "why_it_matters": "Lighting is the architecture of mood - it tells you how to feel about reality",
            "examples": {
                "1-2": ["Nomadland", "Boyhood", "Manchester by the Sea"],
                "description_low": "Natural, ambient, documentary - the world as it is, unmanipulated",
                "viewer_resonance_low": "Viewers who trust reality, who want authenticity over artifice",
                "6-7": ["The Third Man", "Blade Runner 2049", "The Batman"],
                "description_high": "High contrast shadows, sculptural light - reality as psychological landscape",
                "viewer_resonance_high": "Viewers who want cinema as dream, who see emotion in shadows"
            }
        },
        
        "camera_movement_personality": {
            "scale": "1 (locked down, static observation) → 7 (kinetic, handheld chaos)",
            "what_it_measures": "The camera's relationship to the subject - distant witness or intimate participant",
            "why_it_matters": "Movement is empathy. It dictates how close we get to inner life",
            "examples": {
                "1-2": ["Ozu's films", "Paris, Texas", "First Reformed"],
                "description_low": "Still, contemplative, respectful distance - observation without judgment",
                "viewer_resonance_low": "Viewers who want to think, not feel. Who value meditation over immersion",
                "6-7": ["Uncut Gems", "Good Time", "Children of Men"],
                "description_high": "Frenetic, breathing, urgent - cinema as nervous system",
                "viewer_resonance_high": "Viewers who want visceral experience, who need to feel adrenaline"
            }
        },
        
        "shot_composition_philosophy": {
            "scale": "1 (symmetrical, centered, balanced) → 7 (off-balance, diagonal tension)",
            "what_it_measures": "Visual harmony vs visual anxiety - how the frame makes you feel",
            "why_it_matters": "Composition is psychological architecture - it organizes emotional space",
            "examples": {
                "1-2": ["The Grand Budapest Hotel", "2001: A Space Odyssey"],
                "description_low": "Symmetrical, ordered, divine geometry - control and perfection",
                "viewer_resonance_low": "Viewers who find comfort in order, who respond to visual intelligence",
                "6-7": ["The Favourite", "Uncut Gems", "mother!"],
                "description_high": "Chaotic framing, aggressive asymmetry - discomfort as honesty",
                "viewer_resonance_high": "Viewers who want cinema to unsettle, who distrust beauty"
            }
        },
        
        "depth_of_field_psychology": {
            "scale": "1 (deep focus, everything visible) → 7 (shallow, isolated subject)",
            "what_it_measures": "Whether we see context or only the subject - relationality vs isolation",
            "why_it_matters": "Focus is about what matters. Do we live in a world or alone?",
            "examples": {
                "1-2": ["Citizen Kane", "There Will Be Blood"],
                "description_low": "Everything in focus - we are embedded in systems and history",
                "viewer_resonance_low": "Viewers who think systemically, who see interconnection",
                "6-7": ["Lost in Translation", "Her", "The Master"],
                "description_high": "Shallow focus - we are alone, the world blurs behind us",
                "viewer_resonance_high": "Viewers who experience loneliness, who feel unmoored from context"
            }
        },
        
        "texture_and_grain": {
            "scale": "1 (digital pristine) → 7 (heavy grain, analog texture)",
            "what_it_measures": "Material presence of the image - clean vs lived-in reality",
            "why_it_matters": "Texture is memory. Grain is human. Digital is eternal present",
            "examples": {
                "1-2": ["Gemini Man", "The Hobbit", "Billy Lynn's Long Halftime Walk"],
                "description_low": "Hyper-clean, digital perfection - futuristic clarity",
                "viewer_resonance_low": "Viewers who want escapism, who distrust nostalgia",
                "6-7": ["The Florida Project", "Moonlight", "Never Rarely Sometimes Always"],
                "description_high": "Film grain, texture, material presence - cinema as memory object",
                "viewer_resonance_high": "Viewers who romanticize the past, who want cinema to feel tactile"
            }
        },
        
        "aspect_ratio_emotional_frame": {
            "scale": "1 (widescreen epic space) → 7 (boxy intimate 4:3 portrait)",
            "what_it_measures": "The shape of human experience - sprawling landscape or claustrophobic interiority",
            "why_it_matters": "Frame shape is emotional container - it dictates scale of feeling",
            "examples": {
                "1-2": ["Lawrence of Arabia", "The Revenant", "Mad Max Fury Road"],
                "description_low": "Wide epic canvas - we are small in vast spaces",
                "viewer_resonance_low": "Viewers who want grandeur, who respond to sublime scale",
                "6-7": ["First Reformed", "The Lighthouse", "Mommy"],
                "description_high": "Boxy 4:3 - trapped in portrait mode, no escape from self",
                "viewer_resonance_high": "Viewers who live inwardly, who experience life as confinement"
            }
        },
        
        "spatial_density": {
            "scale": "1 (minimalist empty space) → 7 (maximal visual density)",
            "what_it_measures": "Information overload vs contemplative void - how much world we can hold",
            "why_it_matters": "Space is breathing room. Density is anxiety or richness",
            "examples": {
                "1-2": ["Tarkovsky's films", "Gerry", "Hard to Be a God"],
                "description_low": "Vast emptiness, negative space - room for thought",
                "viewer_resonance_low": "Viewers who need silence, who think in stillness",
                "6-7": ["Blade Runner", "Brazil", "Metropolis"],
                "description_high": "Cluttered, overstimulating, cacophonous - world as too much",
                "viewer_resonance_high": "Viewers who live in information overload, who find beauty in chaos"
            }
        },
        
        "cinematic_realism_spectrum": {
            "scale": "1 (documentary vérité) → 7 (surreal dreamspace)",
            "what_it_measures": "Relationship to objective reality - record vs reimagine",
            "why_it_matters": "Realism is trust. Surrealism is inner truth vs outer lie",
            "examples": {
                "1-2": ["The Florida Project", "Winter's Bone", "Wendy and Lucy"],
                "description_low": "Observational realism - life as it is, unadorned",
                "viewer_resonance_low": "Viewers who value authenticity, who distrust manipulation",
                "6-7": ["Mulholland Drive", "Holy Motors", "Synecdoche, New York"],
                "description_high": "Dreamlike, logic-defying - subconscious as more real than surface",
                "viewer_resonance_high": "Viewers who live internally, who experience life as subjective"
            }
        },
        
        "blocking_and_performance_space": {
            "scale": "1 (naturalistic actor movement) → 7 (choreographed, theatrical blocking)",
            "what_it_measures": "Are actors people or symbols? Realism vs ritual",
            "why_it_matters": "Performance style reveals whether we believe in the real or the archetypal",
            "examples": {
                "1-2": ["Cassavetes films", "Blue Valentine", "Krisha"],
                "description_low": "Actors move like humans - messy, unchoreographed life",
                "viewer_resonance_low": "Viewers who want raw emotion, who distrust artifice",
                "6-7": ["Wes Anderson films", "Dogville", "The Favourite"],
                "description_high": "Geometric blocking, stylized movement - humans as chess pieces",
                "viewer_resonance_high": "Viewers who see life as performance, who love formalism"
            }
        },
        
        "color_temperature": {
            "scale": "1 (cold blue clinical) → 7 (warm amber intimate)",
            "what_it_measures": "Emotional warmth vs emotional distance in color tone",
            "why_it_matters": "Warm = human connection. Cold = alienation or clarity",
            "examples": {
                "1-2": ["Minority Report", "Gattaca", "Ex Machina"],
                "description_low": "Blue, sterile, technological - emotion at distance",
                "viewer_resonance_low": "Viewers who intellectualize feeling, who prefer analysis",
                "6-7": ["Amélie", "Moonrise Kingdom", "Carol"],
                "description_high": "Golden hour glow, candlelight warmth - nostalgia and safety",
                "viewer_resonance_high": "Viewers who romanticize, who seek emotional refuge"
            }
        },
        
        "lens_distortion_and_perspective": {
            "scale": "1 (natural human eye perspective) → 7 (extreme wide angle distortion)",
            "what_it_measures": "Perceptual stability vs perceptual unreliability",
            "why_it_matters": "Distortion reveals whether we trust our own perception",
            "examples": {
                "1-2": ["Before Sunrise", "Lady Bird", "Paterson"],
                "description_low": "Normal focal length - the world as we see it",
                "viewer_resonance_low": "Viewers who trust direct experience",
                "6-7": ["Enter the Void", "The Lighthouse", "Requiem for a Dream"],
                "description_high": "Fisheye, extreme perspective - reality as subjective distortion",
                "viewer_resonance_high": "Viewers who experience dissociation, who question reality"
            }
        },
        
        "shadow_ratio": {
            "scale": "1 (low contrast even lighting) → 7 (high contrast deep shadows)",
            "what_it_measures": "Emotional clarity vs ambiguity in light and dark",
            "why_it_matters": "Shadows hide things. Are we comfortable with mystery?",
            "examples": {
                "1-2": ["Nancy Meyers films", "La La Land", "Little Women"],
                "description_low": "Everything visible, no secrets - optimism and clarity",
                "viewer_resonance_low": "Viewers who want comfort, who avoid darkness",
                "6-7": ["The Lighthouse", "Under the Skin", "Only God Forgives"],
                "description_high": "Deep blacks, obscured faces - we live in unknowing",
                "viewer_resonance_high": "Viewers drawn to mystery, who embrace ambiguity"
            }
        },
        
        "frame_rate_and_motion": {
            "scale": "1 (24fps cinematic dreamstate) → 7 (high frame rate hyper-real)",
            "what_it_measures": "Cinema as dream vs cinema as present moment",
            "why_it_matters": "Frame rate is temporal texture - smooth = dream, stuttered = reality",
            "examples": {
                "1-2": ["Most traditional cinema", "In the Mood for Love"],
                "description_low": "24fps motion blur - we accept cinema as dream",
                "viewer_resonance_low": "Viewers who want escape from reality",
                "6-7": ["Billy Lynn's Long Halftime Walk", "Gemini Man"],
                "description_high": "60fps+ clarity - uncomfortable presence of the real",
                "viewer_resonance_high": "Viewers who reject cinema's lies, who want truth"
            }
        },
        
        "visual_motif_repetition": {
            "scale": "1 (varied, no recurring imagery) → 7 (obsessive visual themes)",
            "what_it_measures": "Conscious artistry vs invisible craft - do we notice the director?",
            "why_it_matters": "Repetition makes us aware we're watching art, not life",
            "examples": {
                "1-2": ["Minding the Gap", "The Rider"],
                "description_low": "No self-conscious style - transparency of form",
                "viewer_resonance_low": "Viewers who want immersion over analysis",
                "6-7": ["Wes Anderson films", "Yorgos Lanthimos films"],
                "description_high": "Recurring visual motifs - we are watching a designed object",
                "viewer_resonance_high": "Viewers who love formalism, who watch for craft"
            }
        }
    },
    
    # ═══════════════════════════════════════════════════════════════
    # B. EDITING & RHYTHM (8 dimensions)
    # ═══════════════════════════════════════════════════════════════
    
    "editing_rhythm": {
        
        "editing_tempo": {
            "scale": "1 (meditative long takes) → 7 (jagged hyper-montage)",
            "what_it_measures": "How the film breathes - slow contemplation vs rapid fragmentation",
            "why_it_matters": "Editing is heartbeat. Slow = meditation. Fast = anxiety or ecstasy",
            "examples": {
                "1-2": ["Jeanne Dielman", "Stalker", "Uncle Boonmee"],
                "description_low": "Long unbroken takes - we sit with duration, we wait",
                "viewer_resonance_low": "Viewers with patience, who meditate on images",
                "6-7": ["Requiem for a Dream", "Whiplash", "Mad Max Fury Road"],
                "description_high": "Rapid cuts, sensory assault - we feel through speed",
                "viewer_resonance_high": "Viewers who live at high velocity, who need stimulation"
            }
        },
        
        "narrative_rhythm": {
            "scale": "1 (even flowing linear) → 7 (staccato episodic chaos)",
            "what_it_measures": "Story tempo - smooth journey vs fractured experience",
            "why_it_matters": "Rhythm shapes how we process emotion - gradual vs sudden",
            "examples": {
                "1-2": ["Before trilogy", "The Tree of Life"],
                "description_low": "Gentle accumulation of feeling - time as river",
                "viewer_resonance_low": "Viewers who savor slow revelation",
                "6-7": ["Pulp Fiction", "Dunkirk", "Primer"],
                "description_high": "Fragmented, puzzle-like - we must assemble meaning",
                "viewer_resonance_high": "Viewers who enjoy intellectual work, who distrust linear narrative"
            }
        },
        
        "temporal_structure": {
            "scale": "1 (chronological linear time) → 7 (nonlinear dream logic)",
            "what_it_measures": "Trust in clock time vs time as memory/emotion",
            "why_it_matters": "Linear time = causality. Nonlinear = how memory actually works",
            "examples": {
                "1-2": ["12 Angry Men", "The Social Network"],
                "description_low": "A to B to C - clear cause and effect",
                "viewer_resonance_low": "Viewers who want clarity, who think logically",
                "6-7": ["Eternal Sunshine", "Memento", "The Tree of Life"],
                "description_high": "Time as mosaic - past and present collapse",
                "viewer_resonance_high": "Viewers who experience time as fluid, who live in memory"
            }
        },
        
        "montage_philosophy": {
            "scale": "1 (invisible continuity editing) → 7 (Eisensteinian collision montage)",
            "what_it_measures": "Editing as transparency vs editing as statement",
            "why_it_matters": "Do we notice the cuts? Are we meant to?",
            "examples": {
                "1-2": ["Most Hollywood films", "The Bourne Identity"],
                "description_low": "Seamless, invisible - we forget we're watching edits",
                "viewer_resonance_low": "Viewers who want immersion, not awareness",
                "6-7": ["Battleship Potemkin", "Man with a Movie Camera"],
                "description_high": "Jarring juxtaposition - cuts create meaning through collision",
                "viewer_resonance_high": "Viewers who love meta-awareness, who think about form"
            }
        },
        
        "scene_length_variance": {
            "scale": "1 (uniform scene length) → 7 (radical length variation)",
            "what_it_measures": "Predictability vs surprise in temporal structure",
            "why_it_matters": "Rhythm comfort vs rhythm disorientation",
            "examples": {
                "1-2": ["Typical three-act films"],
                "description_low": "Consistent pacing - we know when scenes will end",
                "viewer_resonance_low": "Viewers who like predictability",
                "6-7": ["Phantom Thread", "The Master", "Holy Motors"],
                "description_high": "Some scenes last 30 seconds, others 20 minutes",
                "viewer_resonance_high": "Viewers who embrace uncertainty, who want surprise"
            }
        },
        
        "ellipsis_and_gaps": {
            "scale": "1 (everything shown) → 7 (radical ellipsis, huge gaps)",
            "what_it_measures": "Do we trust the audience to fill gaps?",
            "why_it_matters": "Gaps force active viewing - we must imagine what's missing",
            "examples": {
                "1-2": ["Avengers films", "Most blockbusters"],
                "description_low": "Every plot point explained and shown",
                "viewer_resonance_low": "Viewers who want complete information",
                "6-7": ["The Master", "Holy Motors", "Uncle Boonmee"],
                "description_high": "Huge time jumps, unexplained transitions",
                "viewer_resonance_high": "Viewers who enjoy ambiguity, who fill gaps themselves"
            }
        },
        
        "transition_style": {
            "scale": "1 (hard cuts) → 7 (slow dissolves, fades)",
            "what_it_measures": "Sharpness vs softness in temporal movement",
            "why_it_matters": "Dissolves = memory, dream. Cuts = immediacy, presence",
            "examples": {
                "1-2": ["Most contemporary films"],
                "description_low": "Immediate transitions - we stay in the present",
                "viewer_resonance_low": "Viewers who live in the now",
                "6-7": ["In the Mood for Love", "The Assassination of Jesse James"],
                "description_high": "Lingering dissolves - time becomes liquid",
                "viewer_resonance_high": "Viewers who experience life as dream, who live in nostalgia"
            }
        },
        
        "rhythm_acceleration": {
            "scale": "1 (steady pace throughout) → 7 (builds to frenetic climax)",
            "what_it_measures": "Emotional architecture - flat vs building intensity",
            "why_it_matters": "Do we want cathartic release or consistent meditation?",
            "examples": {
                "1-2": ["Paris, Texas", "Paterson"],
                "description_low": "No climax, even emotional tone - life has no peaks",
                "viewer_resonance_low": "Viewers who distrust drama, who seek equilibrium",
                "6-7": ["Whiplash", "Black Swan", "Uncut Gems"],
                "description_high": "Building pressure until explosion - cathartic intensity",
                "viewer_resonance_high": "Viewers who need emotional climax, who want release"
            }
        }
    },
    
    # ═══════════════════════════════════════════════════════════════
    # C. SOUND DESIGN & SCORE (9 dimensions)
    # ═══════════════════════════════════════════════════════════════
    
    "sound_and_score": {
        
        "score_emotional_temperature": {
            "scale": "1 (melancholic strings, minor key sorrow) → 7 (triumphant brass, major key joy)",
            "what_it_measures": "Does music amplify sadness or fight it?",
            "why_it_matters": "Score tells us how to feel about what we're seeing",
            "examples": {
                "1-2": ["Requiem for a Dream", "Moonlight", "The Assassination of Jesse James"],
                "description_low": "Mournful, elegiac - we're invited to grieve",
                "viewer_resonance_low": "Viewers who process through melancholy, who value sorrow",
                "6-7": ["Rocky", "Star Wars", "Up"],
                "description_high": "Soaring, hopeful - we're lifted out of darkness",
                "viewer_resonance_high": "Viewers who seek uplift, who want emotional rescue"
            }
        },
        
        "score_density": {
            "scale": "1 (minimalist, sparse) → 7 (maximalist orchestral saturation)",
            "what_it_measures": "How much music fills emotional space",
            "why_it_matters": "Silence vs presence - do we need emotional scaffolding?",
            "examples": {
                "1-2": ["No Country for Old Men (no score)", "Under the Skin"],
                "description_low": "Minimal or no music - we sit in raw reality",
                "viewer_resonance_low": "Viewers who distrust emotional manipulation",
                "6-7": ["Interstellar", "Dunkirk", "Inception"],
                "description_high": "Wall of sound - music as emotional architecture",
                "viewer_resonance_high": "Viewers who want full immersion, who need emotional guidance"
            }
        },
        
        "music_function": {
            "scale": "1 (emotional amplification) → 7 (ironic counterpoint)",
            "what_it_measures": "Does music agree with image or contradict it?",
            "why_it_matters": "Sync = sincerity. Counterpoint = complexity or irony",
            "examples": {
                "1-2": ["Most romantic films", "The Theory of Everything"],
                "description_low": "Music tells you how to feel - sad scene, sad music",
                "viewer_resonance_low": "Viewers who want clarity, who trust earnestness",
                "6-7": ["Kubrick films", "Goodfellas", "Joker"],
                "description_high": "Happy music over violence - dissonance creates meaning",
                "viewer_resonance_high": "Viewers who distrust surface emotion, who love irony"
            }
        },
        
        "soundscape_texture": {
            "scale": "1 (quiet intimate ambience) → 7 (overwhelming sensory saturation)",
            "what_it_measures": "Volume of world - whisper vs roar",
            "why_it_matters": "Sound = presence. Quiet = interiority. Loud = external overwhelm",
            "examples": {
                "1-2": ["A Ghost Story", "First Reformed", "Phantom Thread"],
                "description_low": "Quiet room tone, breathing, footsteps - we hear thinking",
                "viewer_resonance_low": "Viewers who live inwardly, who value silence",
                "6-7": ["Blade Runner 2049", "Dunkirk", "Mad Max Fury Road"],
                "description_high": "Cacophonous, enveloping - world as sensory assault",
                "viewer_resonance_high": "Viewers who want immersion, who live in stimulation"
            }
        },
        
        "diegetic_vs_nondiegetic_ratio": {
            "scale": "1 (all diegetic, source music only) → 7 (pure score, orchestral omniscience)",
            "what_it_measures": "Is music part of world or external emotional commentary?",
            "why_it_matters": "Diegetic = realism. Non-diegetic = we accept emotional manipulation",
            "examples": {
                "1-2": ["Once", "Inside Llewyn Davis", "A Star Is Born"],
                "description_low": "Music comes from radios, clubs, guitars - it's real",
                "viewer_resonance_low": "Viewers who want groundedness, who distrust artifice",
                "6-7": ["Star Wars", "LOTR", "Most Hollywood films"],
                "description_high": "Orchestral score tells us what's important - god's-eye emotion",
                "viewer_resonance_high": "Viewers who accept cinema's artifice, who want guidance"
            }
        },
        
        "sonic_interiority": {
            "scale": "1 (external world sounds) → 7 (subjective inner soundscape)",
            "what_it_measures": "Do we hear objective reality or character's inner experience?",
            "why_it_matters": "Subjective sound = empathy with interiority",
            "examples": {
                "1-2": ["Typical realist films"],
                "description_low": "We hear what's actually there - cars, voices, rain",
                "viewer_resonance_low": "Viewers who trust external reality",
                "6-7": ["Black Swan", "The Master", "Under the Skin"],
                "description_high": "Distorted, subjective - we hear through damaged perception",
                "viewer_resonance_high": "Viewers who experience dissociation, who feel unmoored"
            }
        },
        
        "silence_as_tool": {
            "scale": "1 (constant sound/score) → 7 (radical use of silence)",
            "what_it_measures": "Can absence of sound carry weight?",
            "why_it_matters": "Silence = space for thought, discomfort, awe",
            "examples": {
                "1-2": ["Most Marvel films - constant score"],
                "description_low": "Always filled - we're never alone with image",
                "viewer_resonance_low": "Viewers who fear silence, who need constant stimulus",
                "6-7": ["2001: A Space Odyssey", "A Quiet Place", "Sound of Metal"],
                "description_high": "Extended silence - we must sit with void",
                "viewer_resonance_high": "Viewers who value contemplation, who sit with discomfort"
            }
        },
        
        "vocal_treatment": {
            "scale": "1 (crisp clear dialogue) → 7 (obscured, murmured, layered voices)",
            "what_it_measures": "Is speech information or texture?",
            "why_it_matters": "Clear = we must understand words. Obscured = voice as music",
            "examples": {
                "1-2": ["Typical Hollywood films"],
                "description_low": "Every word audible - dialogue conveys plot",
                "viewer_resonance_low": "Viewers who value comprehension, who need clarity",
                "6-7": ["The New World", "Upstream Color", "McCabe & Mrs. Miller"],
                "description_high": "Mumbled, overlapping - voice as ambient presence",
                "viewer_resonance_high": "Viewers who accept not knowing, who value mood over meaning"
            }
        },
        
        "rhythmic_percussion": {
            "scale": "1 (no percussion, strings/piano) → 7 (driving drums, anxiety pulse)",
            "what_it_measures": "Heartbeat pressure vs ambient float",
            "why_it_matters": "Percussion = urgency, body, visceral stress",
            "examples": {
                "1-2": ["Amélie", "Pride & Prejudice", "Portrait of a Lady on Fire"],
                "description_low": "Soft strings, piano - we float in emotion",
                "viewer_resonance_low": "Viewers who want gentle immersion",
                "6-7": ["Whiplash", "Dunkirk", "Mad Max Fury Road"],
                "description_high": "Relentless drums - we feel physical urgency",
                "viewer_resonance_high": "Viewers who respond to visceral intensity"
            }
        }
    },
    
    # ═══════════════════════════════════════════════════════════════
    # D. STORY & THEMATIC DEEP STRUCTURE (15 dimensions)
    # ═══════════════════════════════════════════════════════════════
    
    "narrative_psychology": {
        
        "human_condition_focus": {
            "scale": "Loneliness, Identity, Grief, Dread, Meaning-making, Longing, Destruction, Transcendence",
            "what_it_measures": "What fundamental human experience drives the story",
            "why_it_matters": "We gravitate to films that mirror our inner struggles",
            "examples": {
                "loneliness": ["Lost in Translation", "Her", "Paterson"],
                "identity": ["Moonlight", "Portrait of a Lady on Fire", "First Reformed"],
                "grief": ["Manchester by the Sea", "The Father", "Amour"],
                "existential_dread": ["Melancholia", "The Seventh Seal", "Synecdoche New York"],
                "meaning_making": ["Tree of Life", "A Ghost Story", "Uncle Boonmee"],
                "longing": ["In the Mood for Love", "Carol", "Call Me by Your Name"],
                "self_destruction": ["Requiem for a Dream", "Shame", "Leaving Las Vegas"],
                "transcendence": ["2001", "The Fountain", "Under the Skin"]
            }
        },
        
        "philosophical_stance": {
            "scale": "1 (humanist hope) → 7 (nihilist void)",
            "what_it_measures": "Does the film believe people can be good?",
            "why_it_matters": "Our worldview aligns with film's worldview",
            "examples": {
                "1-2": ["It's a Wonderful Life", "Paddington 2", "Everything Everywhere"],
                "description_low": "Humanist - people are fundamentally good, connection is possible",
                "viewer_resonance_low": "Viewers who maintain hope, who believe in change",
                "6-7": ["No Country for Old Men", "The House That Jack Built", "Come and See"],
                "description_high": "Nihilist/cynical - cruelty is default, meaning is illusion",
                "viewer_resonance_high": "Viewers who've seen darkness, who distrust optimism"
            }
        },
        
        "narrative_tension_source": {
            "scale": "1 (internal psychological) → 7 (external systemic)",
            "what_it_measures": "Is conflict in the self or in the world?",
            "why_it_matters": "Where we locate struggle reveals what we think causes suffering",
            "examples": {
                "1-2": ["First Reformed", "Phantom Thread", "The Master"],
                "description_low": "Inner demons, identity crisis, psychological fracture",
                "viewer_resonance_low": "Viewers who see struggle as internal work",
                "6-7": ["Sorry to Bother You", "Parasite", "Do the Right Thing"],
                "description_high": "Systems of oppression, capitalism, structural violence",
                "viewer_resonance_high": "Viewers who see struggle as systemic, political"
            }
        },
        
        "plot_archetype": {
            "scale": "Redemption, Dissolution, Rebirth, Disillusionment, Self-reconciliation, Escape, Descent",
            "what_it_measures": "What psychological journey shape does story follow",
            "why_it_matters": "We're drawn to journeys that mirror our own needs",
            "examples": {
                "redemption": ["The Shawshank Redemption", "A Star is Born"],
                "dissolution": ["Requiem for a Dream", "The Wrestler"],
                "rebirth": ["Moonlight", "Lady Bird", "The Florida Project"],
                "disillusionment": ["Nightcrawler", "There Will Be Blood"],
                "self_reconciliation": ["20th Century Women", "The Farewell"],
                "escape": ["Mad Max Fury Road", "Get Out"],
                "descent": ["Black Swan", "mother!", "Taxi Driver"]
            }
        },
        
        "moral_complexity": {
            "scale": "1 (clear good vs evil) → 7 (everyone is compromised)",
            "what_it_measures": "Moral clarity vs moral ambiguity",
            "why_it_matters": "Black and white vs shades of gray reveals our tolerance for ambiguity",
            "examples": {
                "1-2": ["Star Wars", "LOTR", "Harry Potter"],
                "description_low": "Heroes and villains - we know who to root for",
                "viewer_resonance_low": "Viewers who want moral clarity, who need rightness",
                "6-7": ["The Master", "There Will Be Blood", "The Favourite"],
                "description_high": "No heroes - everyone is selfish, flawed, human",
                "viewer_resonance_high": "Viewers who've experienced moral compromise"
            }
        },
        
        "ending_resolution": {
            "scale": "1 (complete closure) → 7 (radical ambiguity)",
            "what_it_measures": "Do we get answers or must we live with questions?",
            "why_it_matters": "Closure = comfort. Ambiguity = respect for complexity",
            "examples": {
                "1-2": ["Most Hollywood films - all questions answered"],
                "description_low": "We know what happened and what it means",
                "viewer_resonance_low": "Viewers who need resolution, who want satisfaction",
                "6-7": ["The Master", "Take Shelter", "Under the Skin"],
                "description_high": "Open ending - we must decide what it means",
                "viewer_resonance_high": "Viewers who embrace uncertainty, who distrust neat endings"
            }
        },
        
        "power_dynamics": {
            "scale": "1 (individual agency) → 7 (structural determinism)",
            "what_it_measures": "Can one person change their fate or are we trapped?",
            "why_it_matters": "Agency vs determinism - do we believe in free will?",
            "examples": {
                "1-2": ["Rocky", "Erin Brockovich", "The Pursuit of Happyness"],
                "description_low": "One person can overcome - individual triumph",
                "viewer_resonance_low": "Viewers who believe in agency, who need empowerment",
                "6-7": ["Parasite", "Sorry to Bother You", "Winter's Bone"],
                "description_high": "Systems crush individuals - no escape",
                "viewer_resonance_high": "Viewers who see structural inequality, who feel trapped"
            }
        },
        
        "intimacy_scale": {
            "scale": "1 (epic historical scope) → 7 (domestic intimate portrait)",
            "what_it_measures": "Do we zoom out to history or zoom in to interiority?",
            "why_it_matters": "Some want to understand the world, others want to understand the self",
            "examples": {
                "1-2": ["Lawrence of Arabia", "Dunkirk", "1917"],
                "description_low": "History, war, nations - individual as part of larger forces",
                "viewer_resonance_low": "Viewers who think systemically, who want scope",
                "6-7": ["Marriage Story", "The Father", "45 Years"],
                "description_high": "One room, two people, inner life - small is infinite",
                "viewer_resonance_high": "Viewers who value interiority, who see depth in the small"
            }
        },
        
        "dialogue_philosophy": {
            "scale": "1 (naturalistic conversation) → 7 (heightened poetic language)",
            "what_it_measures": "Do people talk like real humans or like symbols?",
            "why_it_matters": "Natural speech = realism. Poetic = life as art",
            "examples": {
                "1-2": ["Before trilogy", "Frances Ha", "Lady Bird"],
                "description_low": "People talk like you and your friends - overlaps, ums, tangents",
                "viewer_resonance_low": "Viewers who value authenticity, who distrust artifice",
                "6-7": ["The Favourite", "The Lighthouse", "Brick"],
                "description_high": "No one talks like this - language as music and symbol",
                "viewer_resonance_high": "Viewers who love stylization, who see life as performance"
            }
        },
        
        "relationship_to_class": {
            "scale": "1 (class invisible) → 7 (class as central)",
            "what_it_measures": "Is economic reality foregrounded or invisible?",
            "why_it_matters": "Class consciousness reveals political awareness",
            "examples": {
                "1-2": ["Most rom-coms - everyone has nice apartments"],
                "description_low": "Money is not discussed, class is assumed neutral",
                "viewer_resonance_low": "Viewers who don't think about economics",
                "6-7": ["Parasite", "Sorry to Bother You", "Nomadland"],
                "description_high": "Class shapes everything - economics is destiny",
                "viewer_resonance_high": "Viewers aware of inequality, who see class everywhere"
            }
        },
        
        "body_and_physicality": {
            "scale": "1 (disembodied, cerebral) → 7 (visceral bodily experience)",
            "what_it_measures": "Are we minds or bodies? Thought or sensation?",
            "why_it_matters": "Some live in head, others in flesh",
            "examples": {
                "1-2": ["My Dinner with Andre", "The Man from Earth", "12 Angry Men"],
                "description_low": "Pure conversation and ideas - bodies are irrelevant",
                "viewer_resonance_low": "Viewers who live intellectually, who value ideas",
                "6-7": ["Climax", "Enter the Void", "Titane"],
                "description_high": "Bodies in pain, pleasure, transformation - flesh as truth",
                "viewer_resonance_high": "Viewers who experience life somatically, who trust sensation"
            }
        },
        
        "relationship_model": {
            "scale": "Connection, Alienation, Codependence, Independence, Fusion, Transaction",
            "what_it_measures": "How do humans relate to each other in this world?",
            "why_it_matters": "Relationship model mirrors our own attachment style",
            "examples": {
                "connection": ["Before Sunrise", "Portrait of a Lady on Fire"],
                "alienation": ["Lost in Translation", "Her", "Under the Skin"],
                "codependence": ["Blue Valentine", "Who's Afraid of Virginia Woolf"],
                "independence": ["Wild", "Into the Wild", "Nomadland"],
                "fusion": ["Call Me by Your Name", "Carol"],
                "transaction": ["The Favourite", "There Will Be Blood"]
            }
        },
        
        "time_relationship": {
            "scale": "1 (present moment urgency) → 7 (historical/memory weight)",
            "what_it_measures": "Do we live now or in accumulated past?",
            "why_it_matters": "Present = youth, urgency. Past = age, nostalgia, grief",
            "examples": {
                "1-2": ["Uncut Gems", "Good Time", "Victoria"],
                "description_low": "Real-time pressure - we can't escape the present",
                "viewer_resonance_low": "Viewers who live in urgency, who can't stop moving",
                "6-7": ["The Tree of Life", "Amour", "45 Years"],
                "description_high": "Memory-soaked, past-haunted - we are our history",
                "viewer_resonance_high": "Viewers who live in nostalgia, who feel weight of time"
            }
        },
        
        "hope_quotient": {
            "scale": "1 (optimistic, change is possible) → 7 (despair, stasis, entropy)",
            "what_it_measures": "Can things get better or are we doomed?",
            "why_it_matters": "Hope vs despair is temperament - what we can tolerate",
            "examples": {
                "1-2": ["Paddington 2", "Everything Everywhere All at Once"],
                "description_low": "Love wins, goodness prevails, tomorrow can be better",
                "viewer_resonance_low": "Viewers who maintain optimism despite evidence",
                "6-7": ["Melancholia", "The Road", "No Country for Old Men"],
                "description_high": "Entropy is inevitable, darkness wins, no escape",
                "viewer_resonance_high": "Viewers who've lost hope, who see only decline"
            }
        },
        
        "political_consciousness": {
            "scale": "1 (apolitical individual story) → 7 (overtly political/systemic)",
            "what_it_measures": "Is this about one person or about power structures?",
            "why_it_matters": "Political awareness shapes what stories we need",
            "examples": {
                "1-2": ["Most personal dramas - politics invisible"],
                "description_low": "Individual psychology divorced from context",
                "viewer_resonance_low": "Viewers who see life as personal not political",
                "6-7": ["Sorry to Bother You", "Do the Right Thing", "Blindspotting"],
                "description_high": "Every personal problem has political roots",
                "viewer_resonance_high": "Viewers who can't unsee power, who think structurally"
            }
        }
    },
    
    # ═══════════════════════════════════════════════════════════════
    # E. QUALITY PROFILE - Cinematic Craft & Intention (8 dimensions)
    # ═══════════════════════════════════════════════════════════════
    # What the viewer perceives as meaningful, satisfying, impressive.
    # NOT about "good vs bad" — about what KIND of intention resonates.
    
    "quality_profile": {
        
        "craft_precision_vs_rawness": {
            "scale": "1 (raw expressiveness) → 7 (craft precision)",
            "what_it_measures": "Polished formal mastery vs emotional immediacy over perfection",
            "why_it_matters": "Some find meaning in meticulous control. Others find authenticity in rough edges. Different theories of what makes cinema powerful.",
            "examples": {
                "1-2": ["Kids", "Tangerine", "Wendy and Lucy", "Dogtooth"],
                "description_low": "Loose framing, handheld urgency, minimal production design, naturalistic performances",
                "viewer_resonance_low": "Feel that craft can get in the way of truth. Value spontaneity, documentary-like immediacy, life captured rather than constructed",
                "6-7": ["There Will Be Blood", "Zodiac", "Barry Lyndon", "Blade Runner 2049"],
                "description_high": "Every frame composed, lighting sculpted, performance calibrated to perfection",
                "viewer_resonance_high": "Find deep satisfaction in visual intelligence and formal rigor. Every choice intentional. Craft IS the meaning"
            }
        },
        
        "art_cinema_vs_pop_cinema_mode": {
            "scale": "1 (art-cinema preference) → 7 (pop-cinema preference)",
            "what_it_measures": "Ambiguity/slowness/minimalism vs clarity/pace/entertainment",
            "why_it_matters": "NOT high/low culture snobbery. Art mode values patience and existential inquiry. Pop mode values momentum and clarity. Both are sophisticated value systems.",
            "examples": {
                "1-2": ["Drive My Car", "Columbus", "Jeanne Dielman", "The Tree of Life"],
                "description_low": "Slow, elliptical, contemplative, resists easy interpretation",
                "viewer_resonance_low": "Find pleasure in opacity, patience, having to work for meaning. Cinema as meditation",
                "6-7": ["John Wick", "Mad Max: Fury Road", "Fast & Furious", "Top Gun: Maverick"],
                "description_high": "Propulsive, clear goals, escalating stakes, visceral satisfaction",
                "viewer_resonance_high": "Find pleasure in momentum, clarity, genre satisfaction. Cinema as kinetic experience"
            }
        },
        
        "narrative_ambition_level": {
            "scale": "1 (purely sensory thrill) → 4 (grounded realism) → 7 (mythic statement)",
            "what_it_measures": "How much 'meaning density' the viewer wants from a film",
            "why_it_matters": "Some want cinema to grapple with Grand Themes. Others want human-scale truth. Others just want sensory pleasure. All valid.",
            "examples": {
                "1-2": ["Furious 7", "Top Gun: Maverick", "The Raid"],
                "description_low": "Sensory cinema — movement, spectacle, visceral pleasure over meaning",
                "viewer_resonance_low": "Don't need symbolic weight. Find joy in pure craft, movement, sensory experience",
                "3-5": ["Blue Valentine", "Still Walking", "Manchester by the Sea"],
                "description_mid": "Human-scale realism — everyday emotional truth, no cosmic metaphors",
                "viewer_resonance_mid": "Want emotional authenticity without philosophical abstraction",
                "6-7": ["The Tree of Life", "The Fountain", "There Will Be Blood", "2001"],
                "description_high": "Mythic ambition — existence, mortality, humanity as concept",
                "viewer_resonance_high": "Want cinema to wrestle with Big Questions. Meaning IS the pleasure"
            }
        },
        
        "irony_sincerity_register": {
            "scale": "1 (sincere earnest) → 7 (ironic self-aware)",
            "what_it_measures": "Emotional directness vs self-aware distance",
            "why_it_matters": "Prevents catastrophic mismatches (recommending Tár to Guardians fans). Irony isn't 'smart' — it's a tonal preference.",
            "examples": {
                "1-2": ["Call Me By Your Name", "Aftersun", "Past Lives", "Moonlight"],
                "description_low": "Unguarded emotion, no winking at camera, takes feelings seriously",
                "viewer_resonance_low": "Need full emotional permission. Ironic distance feels cold or cowardly",
                "6-7": ["The Nice Guys", "The Menu", "Everything Everywhere All At Once"],
                "description_high": "Meta-awareness, genre play, emotional beats undercut with humor",
                "viewer_resonance_high": "Find pure sincerity embarrassing or manipulative. Need ironic cushion"
            }
        },
        
        "emotional_weight_tolerance": {
            "scale": "1 (light comfort) → 4 (mid-range emotional) → 7 (devastating weight)",
            "what_it_measures": "How intense or 'heavy' a film can be before it stops being enjoyable",
            "why_it_matters": "Prevents recommending Grave of the Fireflies to cozy-seekers. Some seek devastation. Others need cinema to feel safe.",
            "examples": {
                "1-2": ["Paddington 2", "Ratatouille", "Amélie", "Chef"],
                "description_low": "Buoyant, warm, restorative, emotionally safe",
                "viewer_resonance_low": "Use cinema for emotional restoration. Darkness feels overwhelming",
                "3-5": ["Lady Bird", "Her", "Brooklyn", "Little Women"],
                "description_mid": "Emotional complexity but ultimately hopeful or bittersweet",
                "viewer_resonance_mid": "Want emotional complexity but need some light",
                "6-7": ["Requiem for a Dream", "Come and See", "Breaking the Waves", "Grave of the Fireflies"],
                "description_high": "Devastating, unrelenting, existentially heavy, emotionally punishing",
                "viewer_resonance_high": "Seek catharsis through devastation. Light films feel trivial"
            }
        },
        
        "performance_style_preference": {
            "scale": "1 (naturalistic behavioral) → 7 (heightened theatrical)",
            "what_it_measures": "Should acting disappear into realism or be visibly 'performed'?",
            "why_it_matters": "Some want to forget they're watching actors. Others love visible craft, big gestures, theatrical presence.",
            "examples": {
                "1-2": ["Kelly Reichardt films", "Dardenne brothers", "mumblecore"],
                "description_low": "Non-actors or naturalistic performances, behavioral minutiae",
                "viewer_resonance_low": "Heightened performance breaks immersion. Want behavioral truth",
                "6-7": ["There Will Be Blood", "The Master", "Phantom Thread"],
                "description_high": "Daniel Day-Lewis mode — big, controlled, visibly 'acting'",
                "viewer_resonance_high": "Love watching actors work. Performance IS the art form"
            }
        },
        
        "script_construction_visibility": {
            "scale": "1 (invisible organic) → 7 (visible architecture)",
            "what_it_measures": "Want to see the screenplay's bones or structure hidden?",
            "why_it_matters": "Some love puzzle-box precision (Nolan, Sorkin). Others want cinema to feel like life happening.",
            "examples": {
                "1-2": ["Nomadland", "Paterson", "Wendy and Lucy"],
                "description_low": "No three-act structure, life just unfolds, slice-of-life",
                "viewer_resonance_low": "Visible structure feels artificial. Want narrative to feel discovered",
                "6-7": ["Knives Out", "Inception", "The Social Network"],
                "description_high": "Visible craft, intricate structure, satisfying mechanics",
                "viewer_resonance_high": "Love seeing the machinery work. Structure IS pleasure"
            }
        },
        
        "auteur_intentionality_desire": {
            "scale": "1 (collaborative process) → 7 (singular vision)",
            "what_it_measures": "Value visible directorial control and artistic ego?",
            "why_it_matters": "Some love feeling singular intelligence (Kubrick, PTA, Nolan). Others prefer collaborative, actor-driven, ensemble cinema.",
            "examples": {
                "1-2": ["Mike Leigh", "Cassavetes", "Robert Altman"],
                "description_low": "Improvisational, ensemble-driven, actor-focused",
                "viewer_resonance_low": "Auteur control feels cold or egotistical. Want human messiness",
                "6-7": ["Kubrick", "Wes Anderson", "Nolan", "Villeneuve"],
                "description_high": "Total control, every frame stamped with directorial vision",
                "viewer_resonance_high": "Love feeling a singular artistic intelligence at work"
            }
        }
    },
    
    # ═══════════════════════════════════════════════════════════════
    # F. EMOTIONAL & PHENOMENOLOGICAL (11 dimensions)
    # ═══════════════════════════════════════════════════════════════
    
    "emotional_resonance": {
        
        "emotional_temperature": {
            "scale": "1 (cold, distant, clinical) → 7 (hot, raw, overwhelming)",
            "what_it_measures": "Emotional intensity permission - can we be messy?",
            "why_it_matters": "Some need distance to feel safe, others need immersion",
            "examples": {
                "1-2": ["The Master", "Ex Machina", "Under the Skin"],
                "description_low": "Removed, observational - emotion at arm's length",
                "viewer_resonance_low": "Viewers who intellectualize feeling, who fear overwhelm",
                "6-7": ["Blue Valentine", "Krisha", "Marriage Story"],
                "description_high": "Screaming, crying, breaking - emotion unfiltered",
                "viewer_resonance_high": "Viewers who need catharsis, who want to feel everything"
            }
        },
        
        "catharsis_availability": {
            "scale": "1 (no release, sustained tension) → 7 (explosive emotional climax)",
            "what_it_measures": "Do we get to cry/scream/release or sit in discomfort?",
            "why_it_matters": "Catharsis = emotional safety valve. Lack = endurance test",
            "examples": {
                "1-2": ["First Reformed", "The Master", "Under the Skin"],
                "description_low": "No release - we leave tense and unresolved",
                "viewer_resonance_low": "Viewers who distrust easy emotion, who value restraint",
                "6-7": ["Whiplash", "Black Swan", "The Florida Project ending"],
                "description_high": "Emotional explosion - we finally break and release",
                "viewer_resonance_high": "Viewers who need permission to feel, who want climax"
            }
        },
        
        "tonal_consistency": {
            "scale": "1 (genre pure, consistent) → 7 (radical genre collision)",
            "what_it_measures": "Does tone stay stable or lurch between modes?",
            "why_it_matters": "Consistency = safety. Collision = life's complexity",
            "examples": {
                "1-2": ["Most genre films - horror stays horror, romance stays romance"],
                "description_low": "We know what kind of film we're in",
                "viewer_resonance_low": "Viewers who want reliability, who fear whiplash",
                "6-7": ["Parasite", "Sorry to Bother You", "Everything Everywhere"],
                "description_high": "Comedy becomes horror becomes grief - emotional whiplash",
                "viewer_resonance_high": "Viewers who embrace complexity, who see life as genre chaos"
            }
        },
        
        "empathy_requirement": {
            "scale": "1 (likable protagonists) → 7 (repellent, difficult characters)",
            "what_it_measures": "Must we like who we're watching?",
            "why_it_matters": "Likability = comfort. Difficulty = we examine our judgment",
            "examples": {
                "1-2": ["Paddington", "Amélie", "The Intouchables"],
                "description_low": "Warm, likable, good people - we root for them easily",
                "viewer_resonance_low": "Viewers who want comfort, who need to like protagonists",
                "6-7": ["Nightcrawler", "The House That Jack Built", "Bad Lieutenant"],
                "description_high": "Monsters, sociopaths, cruel people - we watch in horror",
                "viewer_resonance_high": "Viewers who examine darkness, who don't need likability"
            }
        },
        
        "beauty_priority": {
            "scale": "1 (beauty is essential) → 7 (ugliness as honesty)",
            "what_it_measures": "Must cinema be beautiful or can it be deliberately ugly?",
            "why_it_matters": "Beauty = escape, consolation. Ugliness = refusal to comfort",
            "examples": {
                "1-2": ["The Grand Budapest Hotel", "Her", "La La Land"],
                "description_low": "Every frame is designed for beauty - cinema as art object",
                "viewer_resonance_low": "Viewers who seek beauty, who need aesthetic pleasure",
                "6-7": ["Dancer in the Dark", "Dogville", "Inland Empire"],
                "description_high": "Deliberately ugly, anti-aesthetic - rejects beauty as lie",
                "viewer_resonance_high": "Viewers who distrust beauty, who value raw truth"
            }
        },
        
        "humor_type": {
            "scale": "Warm, Absurdist, Dark, Cringe, None, Deadpan, Slapstick",
            "what_it_measures": "If there's humor, what kind and what does it reveal?",
            "why_it_matters": "Humor style reveals how we cope with existence",
            "examples": {
                "warm": ["Paddington", "Hunt for the Wilderpeople"],
                "absurdist": ["The Lobster", "Swiss Army Man"],
                "dark": ["In Bruges", "Three Billboards"],
                "cringe": ["Uncut Gems", "The Square"],
                "none": ["First Reformed", "The Rider"],
                "deadpan": ["Fargo", "Wes Anderson films"],
                "slapstick": ["Buster Keaton", "Kung Fu Hustle"]
            }
        },
        
        "sensory_immersion": {
            "scale": "1 (cerebral, distant) → 7 (fully immersive sensory experience)",
            "what_it_measures": "Do we think about film or feel through our bodies?",
            "why_it_matters": "Immersion = presence. Distance = analysis",
            "examples": {
                "1-2": ["My Dinner with Andre", "The Man from Earth"],
                "description_low": "Pure ideas - we could listen with eyes closed",
                "viewer_resonance_low": "Viewers who live in thought, who value intellect",
                "6-7": ["Dunkirk", "Mad Max Fury Road", "Gravity"],
                "description_high": "Full sensory assault - we feel in our bodies",
                "viewer_resonance_high": "Viewers who want experience over thought"
            }
        },
        
        "vulnerability_exposure": {
            "scale": "1 (protected, defended characters) → 7 (raw exposed interiority)",
            "what_it_measures": "Do we see people's masks or their naked selves?",
            "why_it_matters": "Vulnerability = intimacy. Protection = safety",
            "examples": {
                "1-2": ["Most action films - characters stay defended"],
                "description_low": "Emotional armor stays on - we see performance",
                "viewer_resonance_low": "Viewers who fear vulnerability, who stay defended",
                "6-7": ["Krisha", "First Reformed", "The Master"],
                "description_high": "Total exposure - we see people break completely",
                "viewer_resonance_high": "Viewers who crave intimacy, who need to see naked truth"
            }
        },
        
        "mystery_comfort": {
            "scale": "1 (all explained) → 7 (radical inexplicability)",
            "what_it_measures": "Can we tolerate not understanding?",
            "why_it_matters": "Explanation = control. Mystery = acceptance of unknowing",
            "examples": {
                "1-2": ["Most Hollywood films - every question answered"],
                "description_low": "Plot explained, motivations clear, no loose ends",
                "viewer_resonance_low": "Viewers who need understanding, who fear confusion",
                "6-7": ["Holy Motors", "Uncle Boonmee", "The Tree of Life"],
                "description_high": "No explanation ever comes - we must accept mystery",
                "viewer_resonance_high": "Viewers who embrace unknowing, who trust confusion"
            }
        },
        
        "artifice_awareness": {
            "scale": "1 (invisible craft, immersion) → 7 (self-conscious meta-cinema)",
            "what_it_measures": "Do we forget we're watching a movie or are we reminded?",
            "why_it_matters": "Immersion = escape. Meta = intellectual engagement",
            "examples": {
                "1-2": ["Most Hollywood films - invisible technique"],
                "description_low": "We forget we're watching a constructed object",
                "viewer_resonance_low": "Viewers who want immersion, who don't want to think about craft",
                "6-7": ["Adaptation", "Synecdoche New York", "Holy Motors"],
                "description_high": "Film about filmmaking - we're always aware it's artifice",
                "viewer_resonance_high": "Viewers who love meta-awareness, who enjoy deconstruction"
            }
        },
        
        "suffering_tolerance": {
            "scale": "1 (suffering avoided or resolved) → 7 (suffering unrelenting)",
            "what_it_measures": "How much pain can we witness without escape?",
            "why_it_matters": "Pain tolerance reveals our need for hope vs our acceptance of tragedy",
            "examples": {
                "1-2": ["Most feel-good films - suffering is brief or redemptive"],
                "description_low": "Pain is temporary, leads to growth, is meaningful",
                "viewer_resonance_low": "Viewers who need hope, who can't watch sustained suffering",
                "6-7": ["Dancer in the Dark", "Requiem for a Dream", "Come and See"],
                "description_high": "Unrelenting suffering, no redemption, only endurance",
                "viewer_resonance_high": "Viewers who've known real pain, who reject false comfort"
            }
        }
    }
}

# Total count: 58 dimensions across 5 major categories
