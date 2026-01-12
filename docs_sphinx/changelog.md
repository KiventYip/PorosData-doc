# Changelog

All notable changes to PorosData-Processor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- 🔒 **Security Enhancements**: ReDoS protection, enhanced logging, unified exception handling
- 🚀 **Performance**: Memory-efficient processing, async support, caching layer
- 🔧 **Architecture**: Plugin marketplace, configuration management, REST API
- 📊 **Features**: Multi-language support, document type recognition, quality metrics
- 🔬 **Research**: LLM integration, dataset generation tools

## [0.2.2] - 2026-01-12

### Added
- ✨ **Unicode Normalization**: Added Unicode character normalization for LLM optimization
- 🛡️ **Enhanced Shield Protection**: Improved content protection mechanisms for code blocks and formulas
- 📚 **Documentation**: Initial Sphinx documentation setup with Read the Docs support
- 🔧 **Configuration System**: YAML-based configuration for processing options

### Changed
- 🔄 **Default Pipeline**: Updated default processing pipeline to include Unicode normalization
- 📦 **Dependencies**: Minimal dependency approach using only Python standard library

### Fixed
- 🐛 **Formula Processing**: Improved handling of complex LaTeX expressions
- 📝 **Citation Normalization**: Better support for various citation formats
- 🔍 **Text Cleaning**: Enhanced pattern matching for academic text

## [0.2.1] - 2025-12-15

### Added
- 🎯 **Advanced LaTeX Cleaning**: Optional cleaning of spaces within mathematical formulas
- 🔌 **Plugin System**: Extensible plugin architecture for custom processing rules
- 📊 **Batch Processing**: Support for processing multiple files in directories
- 🎨 **Code Quality**: Added comprehensive test suite and CI/CD pipeline

### Changed
- 🏗️ **Architecture**: Refactored core classes for better modularity
- 📈 **Performance**: Optimized processing pipeline for better speed

### Fixed
- 🐛 **Encoding Issues**: Resolved UTF-8 handling problems
- 📝 **Documentation**: Fixed inconsistencies in docstrings and examples

## [0.2.0] - 2025-11-01

### Added
- 🚀 **MinerU Integration**: Primary support for processing MinerU PDF parser output
- 🧮 **LaTeX Formula Protection**: Automatic detection and shielding of mathematical expressions
- 🇬🇷 **Greek Letter Conversion**: Convert Greek characters to LaTeX commands
- 📖 **Citation Rules**: Normalize various citation formats to standard styles
- 🏛️ **Document Structure**: Handle chapter numbering and document organization

### Changed
- 🎯 **Core Focus**: Shifted from general text cleaning to AI-for-Science specialization
- 📚 **API Design**: Redesigned TextCleaner class with plugin-based architecture

## [0.1.0] - 2025-08-20

### Added
- ✨ **Initial Release**: Basic text cleaning functionality
- 🔧 **Core Cleaning**: Whitespace normalization, space compression, punctuation fixes
- 📁 **File Processing**: Support for processing text files with various encodings
- 🧪 **Basic Testing**: Initial test suite for core functionality

---

## Development Roadmap

### Version 0.3.0 (Q1 2026) - Security & Reliability
- 🔒 **ReDoS Protection**: Replace vulnerable regex patterns
- 📝 **Logging System**: Implement proper logging framework
- ⚠️ **Exception Handling**: Unified exception hierarchy
- 🛡️ **Input Validation**: Enhanced security checks

### Version 0.4.0 (Q2 2026) - Performance & Architecture
- 🚀 **Async Processing**: Support for asynchronous operations
- 💾 **Memory Optimization**: Streaming processing for large documents
- 🔌 **Plugin Marketplace**: Community plugin ecosystem
- ⚙️ **Configuration**: Advanced configuration management

### Version 0.5.0 (Q3 2026) - Features & Languages
- 🌍 **Multi-language Support**: Extended language coverage
- 📄 **Document Types**: Specialized processing for different document types
- 📊 **Quality Metrics**: Processing quality analysis
- 🤖 **AI Integration**: Enhanced LLM integration features

### Version 0.6.0 (Q4 2026) - Research & Enterprise
- 🔬 **Research Tools**: Advanced dataset generation
- 🏢 **Enterprise Features**: Monitoring, analytics, and compliance
- 🔗 **API Services**: REST API for remote processing
- 📈 **Scalability**: High-throughput processing capabilities

---

## Contributing to Changes

Changes are tracked using the following categories:

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes

### How to Suggest Changes

1. **Bug Reports**: Use GitHub Issues with the "bug" label
2. **Feature Requests**: Use GitHub Issues with the "enhancement" label
3. **Security Issues**: Contact maintainers directly (don't create public issues)
4. **Code Contributions**: Submit Pull Requests following our contribution guidelines

---

*For older versions, see the [Git history](https://github.com/KiventYip/porosdata-processor/commits/main) or check the release tags.*