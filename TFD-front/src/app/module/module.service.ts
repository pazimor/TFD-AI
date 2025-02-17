import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Module } from './module.model';

@Injectable({
  providedIn: 'root'
})
export class ModuleService {
  private apiUrl = 'http://localhost:4201/api/modules/ui';

  constructor(private http: HttpClient) { }

  getObjects(): Observable<Module[]> {
    return this.http.get<Module[]>(this.apiUrl); //observable
  }


  filteredObjects(ToFilter: Module[], lang: string | undefined, searchTerm: string): Module[] {
    return ToFilter.filter(obj => obj.name[lang ?? "fr"].toLowerCase().includes(searchTerm.toLowerCase()));
  }
}

