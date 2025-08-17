# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based disaster response manual website for dialysis patients in Fukui Prefecture, Japan. The site is designed to provide comprehensive disaster preparedness and response guidance for dialysis patients, their families, and medical professionals.

## Site Structure and Content

The project is organized as a Jekyll static site with Japanese content:

- **Main site**: `/fukuitouseki.com/` - Jekyll site root
- **Documentation**: `/fukuitouseki.com/docs/` - Manual content organized in phases:
  - `00-preparation.md` - Pre-disaster preparation
  - `01-initial-response.md` - Initial disaster response  
  - `02-facility-response.md` - Facility-specific responses
  - `03-network-coordination.md` - Network coordination
  - `index.md` - Manual table of contents
- **References**: `/references/` - Reference materials from other prefectures

## Jekyll Configuration

The site uses Jekyll with the following key settings:
- **Theme**: minima
- **Language**: Japanese (ja)
- **Timezone**: Asia/Tokyo
- **Plugins**: jekyll-feed, jekyll-sitemap
- **Markdown**: kramdown with rouge highlighter

## Development Commands

Since this is a Jekyll site, typical commands would be:
```bash
# Install dependencies (if Gemfile exists)
bundle install

# Serve locally
bundle exec jekyll serve

# Build site
bundle exec jekyll build
```

Note: No Gemfile was found in the current repository structure, so Jekyll may need to be set up if local development is required.

## Content Guidelines

- All content is in Japanese
- Focus on disaster preparedness for dialysis patients
- Organized in a phase-based response structure (0-3 stages)
- Target audience includes medical professionals, patients, families, and administrators
- Content should be practical and actionable for disaster scenarios

## Git Commit Guidelines

When working with this Japanese content repository:

- **Commit messages**: Write commit messages and comments in Japanese when adding or modifying Japanese content, templates, or documentation
- **Example**: Instead of "Add initial response templates", use "初動対応用の様式テンプレートを追加"
- **Rationale**: Since this is a Japanese disaster response manual for Japanese medical professionals, commit messages in Japanese provide better context and accessibility for the intended audience

## File Locations

- Site configuration: `fukuitouseki.com/_config.yml`
- Main content: `fukuitouseki.com/docs/*.md`
- Site index: `fukuitouseki.com/index.md`
- Project overview: `fukuitouseki.com/README.md`