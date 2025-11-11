import React from "react";
import { 
  Box, 
  Typography, 
  Chip, 
  Button, 
  Stack,
  Card,
  CardContent
} from "@mui/material";
import { 
  AccessTime, 
  CheckCircle, 
  ErrorOutline, 
  Add,
  Description,
  CompareArrows
} from "@mui/icons-material";

const statusColors = {
  pending: "warning",
  running: "info", 
  completed: "success",
  error: "error",
};

const statusIcons = {
  pending: <AccessTime fontSize="small" />,
  running: <AccessTime fontSize="small" />,
  completed: <CheckCircle fontSize="small" />,
  error: <ErrorOutline fontSize="small" />,
};

const GaGaResultHeader = ({ latestComparison, onViewResult, onStart }) => {
  if (!latestComparison) {
    return (
      <Card 
        variant="outlined"
        sx={{
          mb: 3,
          background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
          border: '1px solid',
          borderColor: 'grey.200',
          borderRadius: 2,
          boxShadow: '0 1px 3px 0px rgba(0,0,0,0.05)'
        }}
      >
        <CardContent sx={{ p: 3 }}>
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Box>
              <Typography variant="h6" fontWeight="600" color="grey.800" gutterBottom>
                Ready for GA vs GA Comparison
              </Typography>
              <Typography variant="body2" color="grey.600">
                Start your first GA vs GA comparison to see results here.
              </Typography>
            </Box>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={onStart}
              sx={{
                borderRadius: 2,
                px: 3,
                py: 1,
                fontWeight: '600',
                background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #2563eb 0%, #1e40af 100%)',
                }
              }}
            >
              Start New Comparison
            </Button>
          </Stack>
        </CardContent>
      </Card>
    );
  }

  const { ga1_file_name, ga2_file_name, status, comparison_result_path, updated_at } =
    latestComparison;

  const statusIcon = statusIcons[status] || <AccessTime fontSize="small" />;
  const statusColor = statusColors[status] || "default";

  return (
    <Card 
      variant="outlined"
      sx={{
        mb: 3,
        background: 'white',
        border: '1px solid',
        borderColor: 'grey.200',
        borderRadius: 2,
        boxShadow: '0 1px 3px 0px rgba(0,0,0,0.05)',
        transition: 'all 0.2s ease-in-out',
        '&:hover': {
          boxShadow: '0 4px 12px 0px rgba(0,0,0,0.08)',
        }
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
          <Box sx={{ flex: 1 }}>
            <Stack direction="row" alignItems="center" spacing={1} mb={1.5}>
              <CompareArrows color="primary" fontSize="small" />
              <Typography variant="h6" fontWeight="600" color="grey.800">
                Latest GA vs GA Comparison
              </Typography>
            </Stack>

            {/* File Names */}
            <Stack direction="row" alignItems="center" spacing={2} mb={2}>
              <Box 
                sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  padding: '8px 12px',
                  backgroundColor: 'grey.50',
                  borderRadius: 2,
                  border: '1px solid',
                  borderColor: 'grey.200'
                }}
              >
                <Description sx={{ mr: 1, color: 'primary.main', fontSize: 18 }} />
                <Typography variant="body2" fontWeight="500" color="grey.700">
                  {ga1_file_name}
                </Typography>
              </Box>
              
              <Typography variant="body2" color="grey.500" sx={{ fontStyle: 'italic' }}>
                vs
              </Typography>

              <Box 
                sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  padding: '8px 12px',
                  backgroundColor: 'grey.50',
                  borderRadius: 2,
                  border: '1px solid',
                  borderColor: 'grey.200'
                }}
              >
                <Description sx={{ mr: 1, color: 'secondary.main', fontSize: 18 }} />
                <Typography variant="body2" fontWeight="500" color="grey.700">
                  {ga2_file_name}
                </Typography>
              </Box>
            </Stack>

            {/* Status and Timestamp */}
            <Stack direction="row" alignItems="center" spacing={2}>
              <Chip
                icon={statusIcon}
                label={status.charAt(0).toUpperCase() + status.slice(1)}
                color={statusColor}
                variant="filled"
                size="medium"
                sx={{ 
                  fontWeight: '600',
                  borderRadius: 1.5
                }}
              />
              
              {updated_at && (
                <Typography variant="caption" color="grey.600" sx={{ fontStyle: 'italic' }}>
                  Updated: {new Date(updated_at).toLocaleString()}
                </Typography>
              )}
            </Stack>
          </Box>

          {/* Action Buttons */}
          <Stack direction="row" spacing={1.5} sx={{ ml: 2 }}>
            {status === "completed" && comparison_result_path && (
              <Button
                variant="outlined"
                color="primary"
                size="medium"
                onClick={() => onViewResult(comparison_result_path)}
                sx={{
                  borderRadius: 2,
                  px: 2,
                  fontWeight: '500',
                  borderWidth: '1.5px',
                  '&:hover': {
                    borderWidth: '1.5px'
                  }
                }}
              >
                View Result
              </Button>
            )}

            <Button
              variant="contained"
              color="primary"
              size="medium"
              startIcon={<Add />}
              onClick={onStart}
              sx={{
                borderRadius: 2,
                px: 3,
                fontWeight: '600',
                background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #2563eb 0%, #1e40af 100%)',
                }
              }}
            >
              New Comparison
            </Button>
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
};

export default GaGaResultHeader;
