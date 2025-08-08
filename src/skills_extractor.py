"""
Advanced Skills Extraction Engine
Provides context-aware skill extraction with fuzzy matching and normalization
"""

import logging
import re
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass
from rapidfuzz import fuzz, process
import spacy
from spacy.matcher import PhraseMatcher, Matcher
from spacy.tokens import Doc, Span

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SkillMatch:
    """Represents a skill match with context"""
    skill: str
    confidence: float
    context: str
    position: Tuple[int, int]
    version: str = ""
    normalized: str = ""

class AdvancedSkillsExtractor:
    """Advanced skills extraction with context awareness and fuzzy matching"""
    
    def __init__(self):
        """Initialize the advanced skills extractor"""
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found. Installing...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize skill ontology
        self.skill_ontology = self._build_skill_ontology()
        
        # Initialize matchers
        self._setup_matchers()
        
        logger.info("Advanced Skills Extractor initialized")
    
    def _build_skill_ontology(self) -> Dict[str, Dict[str, Any]]:
        """Build comprehensive skill ontology with synonyms and variations"""
        return {
            # iOS Development
            'swift': {
                'variations': ['swift', 'swiftui', 'swift ui', 'swift 5.x', 'swift 4.x', 'swift 3.x'],
                'synonyms': ['swift programming', 'swift language', 'swift development'],
                'category': 'programming_language',
                'weight': 1.0
            },
            'swiftui': {
                'variations': ['swiftui', 'swift ui', 'swiftui framework'],
                'synonyms': ['swift ui', 'swift user interface'],
                'category': 'framework',
                'weight': 0.9
            },
            'uikit': {
                'variations': ['uikit', 'ui kit', 'cocoa touch'],
                'synonyms': ['user interface kit', 'ios ui framework'],
                'category': 'framework',
                'weight': 0.9
            },
            'cocoa touch': {
                'variations': ['cocoa touch', 'cocoatouch'],
                'synonyms': ['ios framework', 'apple framework'],
                'category': 'framework',
                'weight': 0.8
            },
            
            # Development Tools
            'xcode': {
                'variations': ['xcode', 'xcode 14', 'xcode 15', 'xcode cloud'],
                'synonyms': ['apple ide', 'ios development environment'],
                'category': 'development_tool',
                'weight': 0.8
            },
            'fastlane': {
                'variations': ['fastlane', 'fast lane', 'fast-lane'],
                'synonyms': ['automation tool', 'ci/cd tool'],
                'category': 'devops',
                'weight': 0.7
            },
            'jenkins': {
                'variations': ['jenkins', 'jenkins ci'],
                'synonyms': ['continuous integration', 'ci server'],
                'category': 'devops',
                'weight': 0.7
            },
            
            # Testing
            'xctest': {
                'variations': ['xctest', 'xc test', 'xctestcase'],
                'synonyms': ['unit testing', 'ios testing'],
                'category': 'testing',
                'weight': 0.8
            },
            'xcuitest': {
                'variations': ['xcuitest', 'xcui test', 'ui testing'],
                'synonyms': ['ui testing', 'interface testing'],
                'category': 'testing',
                'weight': 0.8
            },
            
            # Cloud & APIs
            'firebase': {
                'variations': ['firebase', 'firebase analytics', 'firebase crashlytics'],
                'synonyms': ['google firebase', 'mobile backend'],
                'category': 'cloud',
                'weight': 0.7
            },
            'aws': {
                'variations': ['aws', 'amazon web services', 'aws iot'],
                'synonyms': ['amazon cloud', 'cloud computing'],
                'category': 'cloud',
                'weight': 0.7
            },
            'azure': {
                'variations': ['azure', 'microsoft azure', 'azure iot'],
                'synonyms': ['microsoft cloud', 'azure cloud'],
                'category': 'cloud',
                'weight': 0.7
            },
            
            # Authentication & Security
            'oauth': {
                'variations': ['oauth', 'oauth 2.0', 'oauth2'],
                'synonyms': ['authentication', 'authorization'],
                'category': 'security',
                'weight': 0.8
            },
            'jwt': {
                'variations': ['jwt', 'json web token'],
                'synonyms': ['token authentication', 'bearer token'],
                'category': 'security',
                'weight': 0.7
            },
            
            # Architecture Patterns
            'mvvm': {
                'variations': ['mvvm', 'model view viewmodel'],
                'synonyms': ['architecture pattern', 'design pattern'],
                'category': 'architecture',
                'weight': 0.8
            },
            'mvc': {
                'variations': ['mvc', 'model view controller'],
                'synonyms': ['architecture pattern', 'design pattern'],
                'category': 'architecture',
                'weight': 0.8
            },
            'viper': {
                'variations': ['viper', 'viper architecture'],
                'synonyms': ['clean architecture', 'ios architecture'],
                'category': 'architecture',
                'weight': 0.8
            },
            
            # Core iOS Frameworks
            'core data': {
                'variations': ['core data', 'coredata', 'core data framework'],
                'synonyms': ['data persistence', 'ios database'],
                'category': 'framework',
                'weight': 0.8
            },
            'core animation': {
                'variations': ['core animation', 'coreanimation'],
                'synonyms': ['ios animation', 'animation framework'],
                'category': 'framework',
                'weight': 0.7
            },
            'core graphics': {
                'variations': ['core graphics', 'coregraphics'],
                'synonyms': ['ios graphics', 'graphics framework'],
                'category': 'framework',
                'weight': 0.7
            },
            'healthkit': {
                'variations': ['healthkit', 'health kit'],
                'synonyms': ['health framework', 'ios health'],
                'category': 'framework',
                'weight': 0.7
            },
            'arkit': {
                'variations': ['arkit', 'ar kit'],
                'synonyms': ['augmented reality', 'ar framework'],
                'category': 'framework',
                'weight': 0.7
            },
            'mapkit': {
                'variations': ['mapkit', 'map kit'],
                'synonyms': ['mapping framework', 'ios maps'],
                'category': 'framework',
                'weight': 0.7
            },
            'vision framework': {
                'variations': ['vision framework', 'vision', 'computer vision'],
                'synonyms': ['image processing', 'machine learning'],
                'category': 'framework',
                'weight': 0.7
            },
            'coreimage': {
                'variations': ['coreimage', 'core image'],
                'synonyms': ['image processing', 'ios image'],
                'category': 'framework',
                'weight': 0.7
            },
            'storekit': {
                'variations': ['storekit', 'store kit'],
                'synonyms': ['in-app purchases', 'app store payments'],
                'category': 'framework',
                'weight': 0.7
            },
            
            # Authentication & Biometrics
            'face id': {
                'variations': ['face id', 'faceid'],
                'synonyms': ['biometric authentication', 'face recognition'],
                'category': 'security',
                'weight': 0.8
            },
            'touch id': {
                'variations': ['touch id', 'touchid'],
                'synonyms': ['fingerprint authentication', 'biometric auth'],
                'category': 'security',
                'weight': 0.8
            },
            'keychain': {
                'variations': ['keychain', 'keychain services'],
                'synonyms': ['secure storage', 'password management'],
                'category': 'security',
                'weight': 0.7
            },
            
            # Networking & APIs
            'restful apis': {
                'variations': ['restful apis', 'rest api', 'rest apis', 'restful api'],
                'synonyms': ['api integration', 'web services'],
                'category': 'networking',
                'weight': 0.8
            },
            'graphql': {
                'variations': ['graphql', 'graph ql'],
                'synonyms': ['api query language', 'data query'],
                'category': 'networking',
                'weight': 0.7
            },
            'websockets': {
                'variations': ['websockets', 'websocket'],
                'synonyms': ['real-time communication', 'socket connection'],
                'category': 'networking',
                'weight': 0.7
            },
            'mqtt': {
                'variations': ['mqtt', 'mqtt protocol'],
                'synonyms': ['iot protocol', 'message queuing'],
                'category': 'networking',
                'weight': 0.6
            },
            
            # Testing & Quality
            'unit testing': {
                'variations': ['unit testing', 'unit test', 'unit tests'],
                'synonyms': ['test driven development', 'tdd'],
                'category': 'testing',
                'weight': 0.8
            },
            'integration testing': {
                'variations': ['integration testing', 'integration test'],
                'synonyms': ['system testing', 'end-to-end testing'],
                'category': 'testing',
                'weight': 0.7
            },
            'ui testing': {
                'variations': ['ui testing', 'ui test', 'user interface testing'],
                'synonyms': ['interface testing', 'gui testing'],
                'category': 'testing',
                'weight': 0.7
            },
            'automated testing': {
                'variations': ['automated testing', 'automated test', 'test automation'],
                'synonyms': ['automation', 'continuous testing'],
                'category': 'testing',
                'weight': 0.7
            },
            'tdd': {
                'variations': ['tdd', 'test driven development'],
                'synonyms': ['unit testing', 'test first'],
                'category': 'testing',
                'weight': 0.8
            },
            'bdd': {
                'variations': ['bdd', 'behavior driven development'],
                'synonyms': ['behavior testing', 'specification testing'],
                'category': 'testing',
                'weight': 0.7
            },
            
            # CI/CD & DevOps
            'ci/cd': {
                'variations': ['ci/cd', 'ci cd', 'continuous integration', 'continuous deployment'],
                'synonyms': ['devops', 'automation'],
                'category': 'devops',
                'weight': 0.8
            },
            'github actions': {
                'variations': ['github actions', 'github action'],
                'synonyms': ['ci/cd pipeline', 'automation'],
                'category': 'devops',
                'weight': 0.7
            },
            'bitrise': {
                'variations': ['bitrise', 'bitrise ci'],
                'synonyms': ['mobile ci/cd', 'automation'],
                'category': 'devops',
                'weight': 0.6
            },
            
            # App Store & Distribution
            'app store connect': {
                'variations': ['app store connect', 'appstore connect'],
                'synonyms': ['app store', 'distribution'],
                'category': 'distribution',
                'weight': 0.7
            },
            'testflight': {
                'variations': ['testflight', 'test flight'],
                'synonyms': ['beta testing', 'app distribution'],
                'category': 'distribution',
                'weight': 0.7
            },
            
            # Performance & Debugging
            'instruments': {
                'variations': ['instruments', 'xcode instruments'],
                'synonyms': ['performance profiling', 'debugging'],
                'category': 'development_tool',
                'weight': 0.6
            },
            'memory management': {
                'variations': ['memory management', 'memory mgmt'],
                'synonyms': ['memory optimization', 'performance'],
                'category': 'performance',
                'weight': 0.7
            },
            'performance profiling': {
                'variations': ['performance profiling', 'performance profile'],
                'synonyms': ['optimization', 'performance analysis'],
                'category': 'performance',
                'weight': 0.6
            },
            'leak detection': {
                'variations': ['leak detection', 'memory leak'],
                'synonyms': ['memory debugging', 'performance'],
                'category': 'performance',
                'weight': 0.6
            },
            
            # Accessibility
            'accessibility': {
                'variations': ['accessibility', 'a11y'],
                'synonyms': ['inclusive design', 'universal design'],
                'category': 'accessibility',
                'weight': 0.8
            },
            'voiceover': {
                'variations': ['voiceover', 'voice over'],
                'synonyms': ['screen reader', 'accessibility'],
                'category': 'accessibility',
                'weight': 0.7
            },
            'dynamic type': {
                'variations': ['dynamic type', 'dynamic text'],
                'synonyms': ['text scaling', 'accessibility'],
                'category': 'accessibility',
                'weight': 0.7
            },
            'wcag': {
                'variations': ['wcag', 'web content accessibility guidelines'],
                'synonyms': ['accessibility standards', 'compliance'],
                'category': 'accessibility',
                'weight': 0.7
            },
            
            # Privacy & Compliance
            'att': {
                'variations': ['att', 'app tracking transparency'],
                'synonyms': ['privacy', 'tracking permission'],
                'category': 'privacy',
                'weight': 0.7
            },
            'idfa': {
                'variations': ['idfa', 'identifier for advertisers'],
                'synonyms': ['advertising identifier', 'privacy'],
                'category': 'privacy',
                'weight': 0.6
            },
            'privacy': {
                'variations': ['privacy', 'data privacy'],
                'synonyms': ['data protection', 'gdpr'],
                'category': 'privacy',
                'weight': 0.7
            },
            'compliance': {
                'variations': ['compliance', 'regulatory compliance'],
                'synonyms': ['gdpr', 'ccpa', 'regulations'],
                'category': 'privacy',
                'weight': 0.6
            },
            
            # Project Management
            'agile': {
                'variations': ['agile', 'agile methodology'],
                'synonyms': ['scrum', 'iterative development'],
                'category': 'project_management',
                'weight': 0.8
            },
            'scrum': {
                'variations': ['scrum', 'scrum methodology'],
                'synonyms': ['agile', 'sprint planning'],
                'category': 'project_management',
                'weight': 0.8
            },
            'sprint planning': {
                'variations': ['sprint planning', 'sprint plan'],
                'synonyms': ['agile planning', 'iteration planning'],
                'category': 'project_management',
                'weight': 0.7
            },
            'backlog grooming': {
                'variations': ['backlog grooming', 'backlog refinement'],
                'synonyms': ['story refinement', 'agile'],
                'category': 'project_management',
                'weight': 0.6
            },
            'retrospectives': {
                'variations': ['retrospectives', 'retro'],
                'synonyms': ['agile retrospective', 'team reflection'],
                'category': 'project_management',
                'weight': 0.6
            },
            
            # Analytics & Monitoring
            'firebase analytics': {
                'variations': ['firebase analytics', 'analytics'],
                'synonyms': ['user analytics', 'app analytics'],
                'category': 'analytics',
                'weight': 0.6
            },
            'crashlytics': {
                'variations': ['crashlytics', 'firebase crashlytics'],
                'synonyms': ['crash reporting', 'error tracking'],
                'category': 'analytics',
                'weight': 0.6
            },
            'google analytics': {
                'variations': ['google analytics', 'ga'],
                'synonyms': ['web analytics', 'user tracking'],
                'category': 'analytics',
                'weight': 0.6
            },
            'performance monitoring': {
                'variations': ['performance monitoring', 'performance monitor'],
                'synonyms': ['app monitoring', 'performance tracking'],
                'category': 'analytics',
                'weight': 0.6
            }
        }
    
    def _setup_matchers(self):
        """Setup spaCy matchers for pattern matching"""
        self.phrase_matcher = PhraseMatcher(self.nlp.vocab)
        self.matcher = Matcher(self.nlp.vocab)
        
        # Add patterns for skill detection
        self._add_skill_patterns()
        self._add_context_patterns()
    
    def _add_skill_patterns(self):
        """Add patterns for direct skill mentions"""
        # Add all skill variations to phrase matcher
        for skill_name, skill_info in self.skill_ontology.items():
            patterns = [self.nlp(text) for text in skill_info['variations']]
            self.phrase_matcher.add(skill_name, patterns)
    
    def _add_context_patterns(self):
        """Add patterns for context-aware skill detection"""
        # Pattern: "Used X for Y" or "Implemented X" or "Developed with X"
        patterns = [
            [{"LOWER": {"IN": ["used", "utilized", "implemented", "developed", "built", "created", "designed"]}}, 
             {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}],
            [{"LOWER": {"IN": ["experience", "proficient", "skilled", "expert", "familiar"]}}, 
             {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}],
            [{"LOWER": {"IN": ["with", "using", "via", "through", "by"]}}, 
             {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}],
            [{"LOWER": {"IN": ["integrated", "configured", "deployed", "maintained"]}}, 
             {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}],
            # New patterns for context-aware detection
            [{"LOWER": {"IN": ["responsible", "responsible for", "in charge of"]}}, 
             {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}],
            [{"LOWER": {"IN": ["worked", "collaborated", "partnered"]}}, 
             {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}],
            [{"LOWER": {"IN": ["developed", "created", "built"]}}, 
             {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}],
            [{"LOWER": {"IN": ["managed", "led", "oversaw"]}}, 
             {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}]
        ]
        
        for pattern in patterns:
            self.matcher.add("SKILL_CONTEXT", [pattern])
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract skills with advanced matching"""
        if not text:
            return {'technical_skills': [], 'soft_skills': [], 'all_skills': []}
        
        # Process text with spaCy
        doc = self.nlp(text.lower())
        
        # Extract skills using multiple methods
        skill_matches = self._extract_with_phrase_matcher(doc)
        skill_matches.extend(self._extract_with_fuzzy_matching(text))
        skill_matches.extend(self._extract_with_context_patterns(doc))
        
        # Fallback: direct keyword matching for comprehensive coverage
        skill_matches.extend(self._extract_with_direct_matching(text))
        
        # Normalize and deduplicate skills
        normalized_skills = self._normalize_skills(skill_matches)
        
        # Categorize skills
        technical_skills = []
        soft_skills = []
        
        for skill in normalized_skills:
            if skill in self.skill_ontology:
                # Check if it's actually a soft skill despite being in ontology
                if self._is_soft_skill(skill):
                    soft_skills.append(skill)
                else:
                    technical_skills.append(skill)
            else:
                # Check if it's a soft skill
                if self._is_soft_skill(skill):
                    soft_skills.append(skill)
        
        return {
            'technical_skills': technical_skills,
            'soft_skills': soft_skills,
            'all_skills': technical_skills + soft_skills
        }
    
    def _extract_with_phrase_matcher(self, doc: Doc) -> List[SkillMatch]:
        """Extract skills using spaCy phrase matcher"""
        matches = []
        
        for match_id, start, end in self.phrase_matcher(doc):
            skill_name = self.nlp.vocab.strings[match_id]
            span = doc[start:end]
            
            matches.append(SkillMatch(
                skill=skill_name,
                confidence=1.0,
                context=span.text,
                position=(start, end)
            ))
        
        return matches
    
    def _extract_with_fuzzy_matching(self, text: str) -> List[SkillMatch]:
        """Extract skills using fuzzy matching with enhanced pattern recognition"""
        matches = []
        
        # Get all possible skill variations
        all_variations = []
        for skill_name, skill_info in self.skill_ontology.items():
            all_variations.extend(skill_info['variations'])
        
        # Use RapidFuzz for fuzzy matching with multiple strategies
        words = text.split()
        
        # Strategy 1: Word-level fuzzy matching
        for word in words:
            # Clean word
            clean_word = re.sub(r'[^\w\s]', '', word.lower())
            if len(clean_word) < 3:
                continue
            
            # Find best matches with multiple scorers
            best_matches_ratio = process.extract(clean_word, all_variations, 
                                              scorer=fuzz.ratio, limit=3)
            best_matches_partial = process.extract(clean_word, all_variations, 
                                                scorer=fuzz.partial_ratio, limit=3)
            best_matches_token = process.extract(clean_word, all_variations, 
                                              scorer=fuzz.token_sort_ratio, limit=3)
            
            # Combine results and find best matches
            all_matches = {}
            for match, score, index in best_matches_ratio + best_matches_partial + best_matches_token:
                if match not in all_matches:
                    all_matches[match] = score
                else:
                    all_matches[match] = max(all_matches[match], score)
            
            # Filter high-confidence matches
            for match, score in all_matches.items():
                if score >= 75:  # Lower confidence threshold for better coverage
                    skill_name = self._find_skill_by_variation(match)
                    if skill_name:
                        matches.append(SkillMatch(
                            skill=skill_name,
                            confidence=score / 100.0,
                            context=word,
                            position=(0, 0)
                        ))
        
        # Strategy 2: Phrase-level matching for multi-word skills
        phrases = self._extract_phrases(text)
        for phrase in phrases:
            if len(phrase.split()) >= 2:  # Multi-word phrases
                best_matches = process.extract(phrase, all_variations, 
                                            scorer=fuzz.partial_ratio, limit=3)
                
                for match, score, index in best_matches:
                    if score >= 80:  # Higher threshold for phrases
                        skill_name = self._find_skill_by_variation(match)
                        if skill_name:
                            matches.append(SkillMatch(
                                skill=skill_name,
                                confidence=score / 100.0,
                                context=phrase,
                                position=(0, 0)
                            ))
        
        # Strategy 3: Version-aware matching
        version_matches = self._extract_version_aware_skills(text)
        matches.extend(version_matches)
        
        return matches
    
    def _extract_phrases(self, text: str) -> List[str]:
        """Extract meaningful phrases from text"""
        phrases = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            # Extract phrases with common patterns
            # Pattern: "X and Y" or "X, Y, and Z"
            and_patterns = re.findall(r'\b(\w+(?:\s+\w+)*)\s+and\s+(\w+(?:\s+\w+)*)\b', sentence, re.IGNORECASE)
            for match in and_patterns:
                phrases.extend(match)
            
            # Pattern: "X, Y, Z" (comma-separated lists)
            comma_patterns = re.findall(r'\b(\w+(?:\s+\w+)*)\s*,\s*(\w+(?:\s+\w+)*)\s*,\s*(\w+(?:\s+\w+)*)\b', sentence, re.IGNORECASE)
            for match in comma_patterns:
                phrases.extend(match)
            
            # Pattern: "X or Y"
            or_patterns = re.findall(r'\b(\w+(?:\s+\w+)*)\s+or\s+(\w+(?:\s+\w+)*)\b', sentence, re.IGNORECASE)
            for match in or_patterns:
                phrases.extend(match)
        
        return phrases
    
    def _extract_version_aware_skills(self, text: str) -> List[SkillMatch]:
        """Extract skills with version information"""
        matches = []
        
        # Version patterns
        version_patterns = [
            r'(\w+)\s+(\d+\.\d+)',  # Swift 5.7
            r'(\w+)\s+(\d+)',        # Xcode 14
            r'(\w+)\s+(\d+\.\d+\.\d+)',  # Version 1.2.3
        ]
        
        for pattern in version_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                skill_candidate = match.group(1).lower()
                version = match.group(2)
                
                # Check if this is a known skill
                skill_name = self._find_skill_by_variation(skill_candidate)
                if skill_name:
                    matches.append(SkillMatch(
                        skill=skill_name,
                        confidence=0.95,  # High confidence for version-specific matches
                        context=f"{skill_candidate} {version}",
                        position=(match.start(), match.end()),
                        version=version
                    ))
        
        return matches
    
    def _extract_with_context_patterns(self, doc: Doc) -> List[SkillMatch]:
        """Extract skills using context patterns with enhanced NLP detection"""
        matches = []
        
        # Method 1: spaCy pattern matching
        for match_id, start, end in self.matcher(doc):
            span = doc[start:end]
            
            # Look for skill mentions in the context
            for skill_name, skill_info in self.skill_ontology.items():
                for variation in skill_info['variations']:
                    if variation in span.text.lower():
                        matches.append(SkillMatch(
                            skill=skill_name,
                            confidence=0.8,  # Lower confidence for context-based matches
                            context=span.text,
                            position=(start, end)
                        ))
                        break
        
        # Method 2: Sentence-level context analysis
        sentence_matches = self._extract_skills_from_sentences(doc)
        matches.extend(sentence_matches)
        
        # Method 3: Responsibility pattern matching
        responsibility_matches = self._extract_skills_from_responsibilities(doc)
        matches.extend(responsibility_matches)
        
        return matches
    
    def _extract_skills_from_sentences(self, doc: Doc) -> List[SkillMatch]:
        """Extract skills from sentence-level context"""
        matches = []
        
        for sent in doc.sents:
            sent_text = sent.text.lower()
            
            # Look for skill mentions in sentences
            for skill_name, skill_info in self.skill_ontology.items():
                for variation in skill_info['variations']:
                    if variation in sent_text:
                        # Check if the sentence contains context indicators
                        context_indicators = [
                            'used', 'utilized', 'implemented', 'developed', 'built',
                            'created', 'designed', 'integrated', 'configured',
                            'experience', 'proficient', 'skilled', 'expert',
                            'responsible', 'managed', 'led', 'oversaw'
                        ]
                        
                        has_context = any(indicator in sent_text for indicator in context_indicators)
                        
                        matches.append(SkillMatch(
                            skill=skill_name,
                            confidence=0.9 if has_context else 0.7,
                            context=sent.text,
                            position=(sent.start, sent.end)
                        ))
                        break
        
        return matches
    
    def _extract_skills_from_responsibilities(self, doc: Doc) -> List[SkillMatch]:
        """Extract skills from responsibility statements"""
        matches = []
        
        # Common responsibility patterns
        responsibility_patterns = [
            r'responsible for\s+([^.]*)',
            r'in charge of\s+([^.]*)',
            r'managed\s+([^.]*)',
            r'led\s+([^.]*)',
            r'oversaw\s+([^.]*)',
            r'developed\s+([^.]*)',
            r'created\s+([^.]*)',
            r'built\s+([^.]*)',
            r'implemented\s+([^.]*)',
            r'integrated\s+([^.]*)',
            r'configured\s+([^.]*)',
            r'deployed\s+([^.]*)',
            r'maintained\s+([^.]*)'
        ]
        
        text = doc.text
        
        for pattern in responsibility_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                responsibility_text = match.group(1).lower()
                
                # Look for skills in the responsibility text
                for skill_name, skill_info in self.skill_ontology.items():
                    for variation in skill_info['variations']:
                        if variation in responsibility_text:
                            matches.append(SkillMatch(
                                skill=skill_name,
                                confidence=0.95,  # High confidence for responsibility-based matches
                                context=match.group(0),
                                position=(match.start(), match.end())
                            ))
                            break
        
        return matches
    
    def _extract_with_direct_matching(self, text: str) -> List[SkillMatch]:
        """Extract skills using direct keyword matching as fallback"""
        matches = []
        text_lower = text.lower()
        
        for skill_name, skill_info in self.skill_ontology.items():
            for variation in skill_info['variations']:
                if variation in text_lower:
                    matches.append(SkillMatch(
                        skill=skill_name,
                        confidence=0.9,  # High confidence for direct matches
                        context=variation,
                        position=(0, 0)
                    ))
                    break  # Only match the first variation to avoid duplicates
        
        return matches
    
    def _find_skill_by_variation(self, variation: str) -> str:
        """Find the main skill name for a given variation"""
        for skill_name, skill_info in self.skill_ontology.items():
            if variation in skill_info['variations']:
                return skill_name
        return ""
    
    def _normalize_skills(self, skill_matches: List[SkillMatch]) -> List[str]:
        """Normalize and deduplicate skills"""
        normalized = set()
        
        for match in skill_matches:
            # Use the main skill name
            normalized.add(match.skill)
        
        return list(normalized)
    
    def _is_soft_skill(self, skill: str) -> bool:
        """Check if a skill is a soft skill"""
        soft_skills = {
            'agile', 'scrum', 'collaboration', 'team', 'leadership', 'communication',
            'problem solving', 'critical thinking', 'adaptability', 'creativity',
            'time management', 'organization', 'attention to detail', 'analytical',
            'strategic thinking', 'mentoring', 'coaching', 'presentation',
            'sprint planning', 'backlog grooming', 'retrospectives'
        }
        
        return skill.lower() in soft_skills
    
    def extract_technical_skills(self, text: str) -> Set[str]:
        """Extract technical skills (backward compatibility)"""
        result = self.extract_skills(text)
        return set(result.get('technical_skills', []))
    
    def extract_soft_skills(self, text: str) -> Set[str]:
        """Extract soft skills (backward compatibility)"""
        result = self.extract_skills(text)
        return set(result.get('soft_skills', []))


if __name__ == "__main__":
    extractor = AdvancedSkillsExtractor()
    print("Advanced Skills Extractor Module")
