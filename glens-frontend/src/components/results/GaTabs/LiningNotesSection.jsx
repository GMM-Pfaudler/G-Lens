import React, { useState } from "react";
import { Box, Typography, Tabs, Tab } from "@mui/material";

const LiningNotesSection = ({ liningSpec, generalNotes }) => {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  // Safer helper to clean up general notes formatting
  const formatGeneralNotes = (notes) => {
    if (!Array.isArray(notes)) return [];
    
    return notes.map(note => {
      if (typeof note !== 'string') return note;
      
      let cleaned = note;
      
      // Only apply fixes if we detect the specific broken patterns
      if (cleaned.match(/\d+\.\s*\n/)) {
        cleaned = cleaned.replace(/(\d+\.)\s*\n\s*/g, '$1 ');
      }
      
      if (cleaned.match(/DIN\s*\n\s*\d/)) {
        cleaned = cleaned.replace(/DIN\s*\n\s*(\d)\s*\n\s*(\d)\s*\n\s*(\d)\s*\n\s*(\d)\s*\n\s*(\d\.)/g, 'DIN $1$2$3$4$5');
        cleaned = cleaned.replace(/DIN\s*\n\s*(\d)\s*\n\s*(\d)\s*\n\s*(\d)\s*\n\s*(\d\.)/g, 'DIN $1$2$3$4');
      }
      
      if (cleaned.match(/\d\s*\n\s*\d\./)) {
        cleaned = cleaned.replace(/(\d)\s*\n\s*(\d\.)/g, '$1$2');
      }
      
      return cleaned;
    });
  };

  const tabStyles = {
    minHeight: '48px',
    textTransform: 'none',
    fontWeight: 'bold',
  };

  const formattedNotes = formatGeneralNotes(generalNotes);

  return (
    <Box sx={{ 
      flex: 1, 
      display: "flex", 
      flexDirection: "column",
      backgroundColor: '#fafafa',
      borderRadius: 1,
      overflow: 'hidden'
    }}>
      {/* Tabs Header - Fixed (no scroll) */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', backgroundColor: 'white', flexShrink: 0 }}>
        <Tabs 
          value={activeTab} 
          onChange={handleTabChange}
          sx={{
            '& .MuiTab-root': tabStyles,
            '& .Mui-selected': {
              color: 'primary.main',
            }
          }}
        >
          <Tab 
            icon="⚙️" 
            iconPosition="start"
            label="Lining Specification" 
            sx={tabStyles}
          />
          <Tab 
            icon="📝" 
            iconPosition="start"
            label="General Notes" 
            sx={tabStyles}
          />
        </Tabs>
      </Box>

      {/* Tab Content - Fixed height container */}
      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
        {activeTab === 0 && (
          <Box sx={{ p: 2, flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            <Typography 
              variant="subtitle1"
              sx={{ 
                mb: 2,
                color: 'primary.main',
                fontWeight: 'bold',
                flexShrink: 0  // Header doesn't scroll
              }}
            >
              Lining Specification
            </Typography>
            {/* Scrollable content box only */}
            <Box sx={{ 
              backgroundColor: 'white',
              p: 2,
              borderRadius: 1,
              border: '1px solid #e0e0e0',
              flex: 1,
              overflow: 'auto',  // Only this box scrolls
              minHeight: 0
            }}>
              {liningSpec ? (
                <Typography sx={{ 
                  whiteSpace: "pre-wrap", 
                  lineHeight: 1.5,
                  fontSize: '0.875rem'
                }}>
                  {liningSpec}
                </Typography>
              ) : (
                <Typography color="text.secondary" fontStyle="italic" fontSize="0.875rem">
                  No lining specification available
                </Typography>
              )}
            </Box>
          </Box>
        )}

        {activeTab === 1 && (
          <Box sx={{ p: 2, flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            <Typography 
              variant="subtitle1"
              sx={{ 
                mb: 2,
                color: 'primary.main',
                fontWeight: 'bold',
                flexShrink: 0  // Header doesn't scroll
              }}
            >
              General Notes
            </Typography>
            {/* Scrollable content box only */}
            <Box sx={{ 
              backgroundColor: 'white',
              p: 2,
              borderRadius: 1,
              border: '1px solid #e0e0e0',
              flex: 1,
              overflow: 'auto',  // Only this box scrolls
              minHeight: 0
            }}>
              {formattedNotes.length > 0 ? (
                <Box>
                  {formattedNotes.map((item, i) => (
                    <Typography
                      key={i}
                      sx={{ 
                        whiteSpace: "pre-wrap", 
                        lineHeight: 1.5,
                        mb: 1.5,
                        fontSize: '0.875rem'
                      }}
                    >
                      {item}
                    </Typography>
                  ))}
                </Box>
              ) : (
                <Typography color="text.secondary" fontStyle="italic" fontSize="0.875rem">
                  No general notes available
                </Typography>
              )}
            </Box>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default LiningNotesSection;