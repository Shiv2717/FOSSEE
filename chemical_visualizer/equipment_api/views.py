"""
Views for equipment API - handles CSV upload, history, and PDF report endpoints.
"""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
import pandas as pd
import json
import io

from equipment_api.models import EquipmentUpload
from equipment_api.serializers import EquipmentUploadSerializer, CSVUploadSerializer
from equipment_api.pdf_utils import generate_equipment_report


class EquipmentUploadViewSet(viewsets.ViewSet):
    """
    ViewSet for equipment CSV upload and history retrieval.
    
    Endpoints:
    - POST /api/upload/ : Upload CSV file
    - GET /api/history/ : Get last 5 uploads
    
    Authentication: Basic Auth required (username/password)
    """
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """
        Upload a CSV file with equipment data.
        
        Expected columns: Equipment Name, Type, Flowrate, Pressure, Temperature
        
        Returns: Upload summary with statistics
        """
        serializer = CSVUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_file = serializer.validated_data['csv_file']
        
        try:
            # Read CSV file
            df = pd.read_csv(io.StringIO(csv_file.read().decode('utf-8')))
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = set(required_columns) - set(df.columns)
            
            if missing_columns:
                return Response(
                    {
                        'error': f"Missing columns: {', '.join(missing_columns)}",
                        'required_columns': required_columns
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Select only required columns and remove rows with NaN values
            df = df[required_columns].dropna()
            
            if len(df) == 0:
                return Response(
                    {'error': 'No valid data found in CSV'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Compute statistics
            equipment_count = len(df)
            avg_flowrate = float(df['Flowrate'].mean())
            avg_pressure = float(df['Pressure'].mean())
            avg_temperature = float(df['Temperature'].mean())
            
            # Equipment type distribution
            type_distribution = df['Type'].value_counts().to_dict()
            type_distribution_json = json.dumps(type_distribution)
            
            # Create upload record
            upload = EquipmentUpload.objects.create(
                filename=csv_file.name,
                equipment_count=equipment_count,
                avg_flowrate=avg_flowrate,
                avg_pressure=avg_pressure,
                avg_temperature=avg_temperature,
                type_distribution=type_distribution_json,
            )
            
            # Cleanup old uploads (keep only last 5)
            EquipmentUpload.cleanup_old_uploads()
            
            # Return the created upload
            serializer = EquipmentUploadSerializer(upload)
            return Response(
                {
                    'message': 'CSV uploaded successfully',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        except pd.errors.ParserError:
            return Response(
                {'error': 'Invalid CSV format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Error processing file: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Retrieve the last 5 uploaded files with their statistics.
        
        Returns: List of uploads ordered by most recent first
        """
        uploads = EquipmentUpload.objects.all()[:5]
        serializer = EquipmentUploadSerializer(uploads, many=True)
        
        return Response(
            {
                'count': len(uploads),
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def report(self, request):
        """
        Generate a PDF report for a specific upload or most recent upload.
        
        Query Parameters:
        - upload_id: Optional. Specific upload ID to generate report for.
                     If not provided, uses most recent upload.
        
        Returns: PDF file as downloadable attachment
        """
        upload_id = request.query_params.get('upload_id')
        
        try:
            if upload_id:
                upload = EquipmentUpload.objects.get(id=upload_id)
            else:
                # Get most recent upload
                upload = EquipmentUpload.objects.first()
                if not upload:
                    return Response(
                        {'error': 'No uploads found. Please upload a CSV file first.'},
                        status=status.HTTP_404_NOT_FOUND
                    )
        except EquipmentUpload.DoesNotExist:
            return Response(
                {'error': f'Upload with ID {upload_id} not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            # Generate PDF
            pdf_content = generate_equipment_report(upload)
            
            # Create response with PDF
            filename = f"equipment_report_{upload.id}.pdf"
            response = FileResponse(
                io.BytesIO(pdf_content),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
        
        except Exception as e:
            return Response(
                {'error': f'Error generating PDF report: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
