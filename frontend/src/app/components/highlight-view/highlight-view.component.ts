import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-highlight-view',
  templateUrl: './highlight-view.component.html',
  styleUrls: ['./highlight-view.component.css']
})
export class HighlightViewComponent {
  @Input() highlightUrl: string = '';
} 