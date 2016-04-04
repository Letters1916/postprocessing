<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs"
    version="1.0">
    <xsl:output method="xml" version="1.0"
        encoding="UTF-8" indent="yes"/>
    <xsl:strip-space elements="tei:revisionDesc tei:correspDesc tei:correspAction tei:list tei:msIdentifier tei:titleStmt tei:facsimile tei:group tei:text tei:body tei:teiHeader tei:TEI tei:editionStmt"/>
    
    <xsl:template match="/">
        <xsl:processing-instruction name="xml">
                <xsl:text>version="1.0" encoding="UTF-8"</xsl:text>
        </xsl:processing-instruction>
        <xsl:processing-instruction name="oxygen">
                <xsl:text>RNGSchema="https://raw.githubusercontent.com/bleierr/Letters-1916-sample-files/master/plain%20corresp%20templates/template.rng" type="xml"</xsl:text>
        </xsl:processing-instruction>
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="processing-instruction()">
        
    </xsl:template>
    
    <xsl:template match="tei:text">
        <xsl:element name="text" namespace="http://www.tei-c.org/ns/1.0">
            <xsl:if test="@type">
            <xsl:attribute name="type">
                <xsl:choose>
                    <xsl:when test="@type='letter'">
                        <xsl:choose>
                            <xsl:when test="not(preceding-sibling::node()[@type='letter'])">
                                <xsl:text>letter</xsl:text>
                            </xsl:when>
                            <xsl:otherwise>additional</xsl:otherwise>
                        </xsl:choose>
                        
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="@type"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            </xsl:if>
            <xsl:if test="@decls">
                <xsl:attribute name="decls">
                    <xsl:value-of select="@decls"/>
                </xsl:attribute>
            </xsl:if>
            
            <xsl:apply-templates></xsl:apply-templates>
        </xsl:element>
        
    </xsl:template>
    
    
    <xsl:template match="tei:facsimile">
        <xsl:copy>
        <xsl:for-each select="tei:graphic">
            <xsl:variable name="facsID" select="@xml:id"></xsl:variable>
            <xsl:choose>
                
                <xsl:when test="count(//tei:pb[substring-after(@facs,'#')=$facsID]) > 1">
                    <xsl:element name="ERROR"></xsl:element>
                    <xsl:element name="graphic" namespace="http://www.tei-c.org/ns/1.0">
                        <xsl:attribute name="xml:id">
                            <xsl:value-of select="@xml:id"/>
                        </xsl:attribute>
                        <xsl:attribute name="url">
                            <xsl:value-of select="@url"/>
                        </xsl:attribute>
                    </xsl:element>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:element name="graphic" namespace="http://www.tei-c.org/ns/1.0">
                        <xsl:attribute name="xml:id">
                            <xsl:value-of select="@xml:id"/>
                        </xsl:attribute>
                        <xsl:attribute name="url">
                            <xsl:value-of select="@url"/>
                        </xsl:attribute>
                    </xsl:element>
                </xsl:otherwise> 
            </xsl:choose>
           
        </xsl:for-each>
        </xsl:copy>
    </xsl:template>
     
    <xsl:template match="tei:pb">
        <xsl:variable name="facsID" select="@facs"></xsl:variable>
        <xsl:choose>
            <xsl:when test="preceding::tei:pb[@facs=$facsID]">
                <xsl:element name="pb" namespace="http://www.tei-c.org/ns/1.0">
                    <xsl:attribute name="facs">
                        <xsl:value-of select="@facs"/><xsl:text>a</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="n">
                        <xsl:value-of select="@n"/>
                    </xsl:attribute>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="pb" namespace="http://www.tei-c.org/ns/1.0">
                    <xsl:attribute name="facs">
                        <xsl:value-of select="@facs"/>
                    </xsl:attribute>
                    <xsl:attribute name="n">
                        <xsl:value-of select="@n"/>
                    </xsl:attribute>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>
    
    <xsl:template match="tei:lb[not(ancestor::tei:p)]">
        
        <xsl:element name="lb" namespace="http://www.tei-c.org/ns/1.0">
            <xsl:attribute name="rend">permanent</xsl:attribute>
        </xsl:element>
        
    </xsl:template>
    
    
    
    
</xsl:stylesheet>