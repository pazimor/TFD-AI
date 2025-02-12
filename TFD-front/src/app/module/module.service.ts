import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {from, Observable} from 'rxjs';
import { Module } from './module.model';

@Injectable({
  providedIn: 'root'
})
export class ModuleService {
  private apiUrl = 'http://localhost:4201/api/modules/ui';

  constructor(
    private http: HttpClient
  ) { }

  getObjects(): Observable<Module[]> {
    return this.http.get<Module[]>(this.apiUrl); //observable
  }
}
