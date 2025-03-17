import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-upload-video',
  templateUrl: './upload-video.component.html',
  styleUrls: ['./upload-video.component.css']
})
export class UploadVideoComponent {
  selectedFile: File | null = null;
  uploadStatus: string = '';
  errorMessage: string = '';

  constructor(private apiService: ApiService) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  uploadVideo() {
    if (this.selectedFile) {
      this.apiService.uploadVideo(this.selectedFile).subscribe({
        next: (response) => {
          this.uploadStatus = 'Upload successful!';
          this.errorMessage = '';
        },
        error: (error) => {
          this.errorMessage = error.error.error || 'Upload failed';
          this.uploadStatus = '';
        }
      });
    }
  }
} 